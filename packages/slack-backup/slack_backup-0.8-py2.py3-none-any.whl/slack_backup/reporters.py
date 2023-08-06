"""
Reporters module.

There are several classes for specific format reporting, and also some of the
slack conversation/convention parsers.
"""
import os
import errno
import html.parser
import logging
import pathlib
import re

from slack_backup import objects as o
from slack_backup import utils
from slack_backup import emoji


class Reporter(object):
    """Base reporter class"""
    ext = ''
    symbols = {'plain': {'join': '->',
                         'leave': '<-',
                         'me': '*',
                         'file': '-',
                         'topic': '+',
                         'separator': '|'},
               'unicode': {'join': '⮊',
                           'leave': '⮈',
                           'me': '🟊',
                           'file': '📂',
                           'topic': '🟅',
                           'separator': '│'}}
    literal_url_pat = re.compile(r'(?P<replace>(?P<url>https?[^\s\|]+))')
    url_pat = re.compile(r'(?P<replace><(?P<url>http[^\|>]+)'
                         r'(\|(?P<title>[^>]+))?>)')
    url2_pat = re.compile(r'<(?P<url>https?[^\s\|]+)>')
    slackid_pat = re.compile(r'(?P<replace><@'
                             r'(?P<slackid>U[A-Z,0-9]+)(\|[^>]+)?[^>]*>)')

    def __init__(self, args, query):
        self.out = args.output
        self.theme = args.theme
        self.q = query
        self.types = {"channel_join": self._msg_join,
                      "channel_leave": self._msg_leave,
                      "channel_topic": self._msg_topic,
                      # "file_share": self._msg_file,
                      "me_message": self._msg_me}

        self.emoji = emoji.EMOJI.get(args.theme, {})

        self.channels = self._get_channels(args.channels)
        self.users = self.q(o.User).all()

    def generate(self):
        """Generate raport for each channel"""
        for channel in self.channels:
            messages = []
            log_path = self.get_log_path(channel.name)
            try:
                os.unlink(log_path)
            except IOError as err:
                if err.errno != errno.ENOENT:
                    raise
            for message in self.q(o.Message).\
                    filter(o.Message.channel == channel).\
                    order_by(o.Message.ts).all():
                messages.append(message)
            self.write_msg(messages, log_path, channel)

    def get_log_path(self, name):
        """Return relative log file name """
        return os.path.join(self.out, name + self.ext)

    def write_msg(self, messages, log, channel):
        """Write message to file"""
        with open(log, "a", encoding='utf8') as fobj:
            for message in messages:
                data = self._process_message(message)
                fobj.write(data['tpl'].format(**data))
                if message.files:
                    for _file in message.files:
                        data = self._msg_file(message, _file)
                        fobj.write(data['tpl'].format(**data))
                # else:
                    # data = self._process_message(message)
                    # fobj.write(data['tpl'].format(**data))

    def _get_symbol(self, item):
        """Return appropriate item depending on the selected theme"""
        return self.symbols[self.theme][item]

    def _get_channels(self, selected_channels):
        """
        Retrieve channels from db and return those which names matched from
        selected_channels list
        """
        all_channels = self.q(o.Channel).all()
        if not selected_channels:
            return all_channels

        result = []
        for channel in all_channels:
            if channel.name in selected_channels:
                result.append(channel)
        return result

    def _process_message(self, msg):
        """
        Make changes to the text (replace slack ids, replace representation of
        urls, substitute images etc) and return dict with data suitable to
        display.
        """
        processor = self.types.get(msg.type, self._msg)
        data = processor(msg)
        data.update({'date': msg.datetime().strftime("%Y-%m-%d %H:%M:%S"),
                     'tpl': "{date} {nick} {msg}"})

        for emoticon in self.emoji:
            data['msg'] = data['msg'].replace(emoticon, self.emoji[emoticon])

        return data

    def _msg_join(self, msg):
        """return data for join"""
        return {'msg': msg.text,
                'nick': self._get_symbol('join')}

    def _msg_leave(self, msg):
        """return data for leave"""
        return {'msg': msg.text,
                'nick': self._get_symbol('leave')}

    def _msg_topic(self, msg):
        """return data for set topic"""
        return {'msg': msg.text,
                'nick': self._get_symbol('topic')}

    def _msg_me(self, msg):
        """return data for /me"""
        return {'msg': msg.user.name + ' ' + msg.text,
                'nick': self._get_symbol('me')}

    def _msg_file(self, msg, _file):
        """return data for file"""
        return {'msg': msg.text,
                'nick': self._get_symbol('file')}

    def _msg(self, msg):
        """return data for all other message types"""
        return {'msg': msg.text,
                'nick': msg.user.name}

    def _filter_slackid(self, text):
        """filter out all of the id from slack"""
        match = True
        while match:
            match = self.slackid_pat.search(text)
            if not match:
                return text

            match = match.groupdict()
            user = self.q(o.User).filter(o.User.slackid ==
                                         match['slackid']).one()
            text = text.replace(match['replace'], user.name)

        return text


class NoneReporter(Reporter):
    """Dummy reporter used for fallback"""

    def generate(self):
        """Generate raport it's a dummmy one - for use with none reporter"""
        return


class TextReporter(Reporter):
    """Text aka IRC reporter"""
    ext = '.log'
    tpl = '{date} {nick:>{max_len}} {separator} {msg}\n'

    def __init__(self, args, query):
        super(TextReporter, self).__init__(args, query)
        utils.makedirs(self.out)
        self._max_len = 0

    def generate(self):
        """Generate raport"""
        for channel in self.channels:
            messages = []
            log_path = self.get_log_path(channel.name)
            self._set_max_len(channel)
            try:
                os.unlink(log_path)
            except IOError as err:
                if err.errno != errno.ENOENT:
                    raise
            for message in self.q(o.Message).\
                    filter(o.Message.channel == channel).\
                    order_by(o.Message.ts).all():
                messages.append(message)

            self.write_msg(messages, log_path, channel)

    def _set_max_len(self, channel):
        """calculate max_len for sepcified channel"""
        users = [m.user for m in channel.messages]
        users = set([u.name for u in users])

        self._max_len = 0
        for user_name in users:
            if len(user_name) > self._max_len:
                self._max_len = len(user_name)

    def _process_message(self, msg):
        """
        Check what kind of message we are dealing with and do appropriate
        formatting
        """
        data = super(TextReporter, self)._process_message(msg)
        data['msg'] = self._filter_slackid(data['msg'])
        data['msg'] = self._fix_newlines(data['msg'])
        data['msg'] = self._remove_entities(data['msg'])
        data.update({'date': msg.datetime().strftime("%Y-%m-%d %H:%M:%S"),
                     'max_len': self._max_len,
                     'separator': self._get_symbol('separator'),
                     'tpl': self.tpl})
        return data

    def _msg_file(self, message, _file):
        """return data for file"""
        if _file.filepath:
            fpath = os.path.abspath(_file.filepath)
            fpath = pathlib.PurePath(fpath).as_uri()
        else:
            fpath = 'does_not_exists'

        return {'msg': _file.title + ' ' + fpath,
                'nick': self._get_symbol('file'),
                'date': message.datetime().strftime("%Y-%m-%d %H:%M:%S"),
                'max_len': self._max_len,
                'separator': self._get_symbol('separator'),
                'tpl': self.tpl}

    def _msg(self, msg):
        """return data for all other message types"""

        data = super(TextReporter, self)._msg(msg)
        result = ''

        if msg.attachments:
            for att in msg.attachments:
                if att.title:
                    att_text = att.title + '\n'
                else:
                    att_text = self._fix_newlines(att.fallback) + '\n'

                if att.text:
                    att_text += att.text

                result += att_text + '\n'

        data['msg'] += result.strip()
        return data

    def _remove_entities(self, text):
        """replace html entites into appropriate chars"""
        return html.parser.HTMLParser().unescape(text)

    def _fix_newlines(self, text):
        """Shift text with new lines to the right with separator"""
        shift = 19  # length of the date
        shift += 1  # separator space
        shift += self._max_len  # length reserved for the nicks
        shift += 1  # separator space
        return text.replace('\n', '\n' + shift * ' ' +
                            self._get_symbol('separator') + ' ')


class StaticHtmlReporter(Reporter):
    """Text-like, but with browsable, clickable links"""
    ext = '.html'
    index_templ = """<!DOCTYPE html>
        <html>
        <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
        <title>%(title)s</title>
        </head>
        <body>
        <div id="container">
        %(msgs)s
        </div>
        </body>
        </html>
    """
    index_list = """
        <ul>
            %s
        </ul>
    """
    msg_head = """<!DOCTYPE html>
        <html>
        <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
        <title>%(title)s</title>
        """
    msg_style = """
        <style>
        * {
            font-family: sans-serif;
        }
        .log {
            width: 100%;
        }
        .log tr:nth-child(even) {
            background-color: #efefef;
        }
        .nick {
            text-align: right;
            white-space: nowrap;
        }
        .date {
            white-space: nowrap;
        }
        td {
            padding: 2px;
        }
        img {
            max-height: 300px;
            max-widht: 500px;
        }
        </style>
        </head>
        <body>
        <div id="container">
        <table class="log">
    """
    msg_foot = """
        </table>
        </div>
        </body>
        </html>
    """
    msg_line = """
            <tr>
                <td class="date">{date}</td>
                <td class="nick">{nick}</td>
                <td>{msg}</td>
            </tr>
        """

    def __init__(self, args, query):
        super(StaticHtmlReporter, self).__init__(args, query)
        utils.makedirs(self.out)
        self._max_len = 0

    def generate(self):
        """Generate raport"""
        super(StaticHtmlReporter, self).generate()

        with open(os.path.join(self.out, "index.html"), "w",
                  encoding='utf8') as fobj:
            content = {'title': 'index',
                       'msgs': self.index_list % self._get_index_list()}
            fobj.write(self.index_templ % content)

    def write_msg(self, messages, log, channel):
        """Write message to file"""
        with open(log, "w", encoding='utf8') as fobj:
            title = channel.name
            if channel.topic:
                title = channel.name + ' ' + channel.topic.value
            fobj.write(self.msg_head % {'title': title})
            fobj.write(self.msg_style)

        super(StaticHtmlReporter, self).write_msg(messages, log, channel)

        with open(log, "a", encoding='utf8') as fobj:
            fobj.write(self.msg_foot)

    def _get_index_list(self):
        _list = []
        for channel in sorted([c.name for c in self.channels]):
            _list.append('<li><a href="%s">%s</a></li>' % (channel + '.html',
                                                           channel))
        return '\n'.join(_list)

    def _process_message(self, msg):
        """
        Check what kind of message we are dealing with and do appropriate
        formatting
        """
        data = super(StaticHtmlReporter, self)._process_message(msg)
        data['msg'] = self._filter_slackid(data['msg'])
        data.update({'date': msg.datetime().strftime("%Y-%m-%d %H:%M:%S"),
                     'tpl': self.msg_line})
        return data

    def _msg_file(self, msg, _file):
        """return data for file"""
        if _file.filepath:
            fpath = os.path.abspath(_file.filepath)
            fpath = pathlib.PurePath(fpath).as_uri()
        else:
            fpath = 'does_not_exists'

        _, ext = os.path.splitext(fpath)
        if ext.lower() in ('.png', '.jpg', '.jpeg', '.gif'):
            url = ('<img src="' + fpath + '" alt="' +
                   _file.title + '">')
        else:
            url = ('<a href="' + fpath + '">' + _file.title + '</a>')

        data = {'date': msg.datetime().strftime("%Y-%m-%d %H:%M:%S"),
                'msg': self._filter_slackid(url + _file.title),
                'tpl': self.msg_line,
                'nick': self._get_symbol('file')}

        for emoticon in self.emoji:
            data['msg'] = data['msg'].replace(emoticon, self.emoji[emoticon])

        return data

    def _msg(self, msg):
        """return processor for all other message types"""

        match = self.url2_pat.match(msg.text)
        text = msg.text
        if match:
            text = ''
            for part in self.url2_pat.split(msg.text):
                if 'http' in part:
                    text += '<a href="' + part + '">' + part + '</a>'
                else:
                    text += part

        data = {'date': msg.datetime().strftime("%Y-%m-%d %H:%M:%S"),
                'msg': text,
                'nick': msg.user.name}

        link = '<a href="{url}">{title}</a>'
        attachment_msg = []

        if msg.attachments:
            for att in msg.attachments:
                if 'http' in att.fallback:
                    match = self.url_pat.search(att.fallback)
                    if not match:
                        match = self.literal_url_pat.search(att.fallback)
                    match = match.groupdict()

                    if 'title' not in match:
                        match['title'] = match['url']
                        if att.title:
                            match['title'] = att.title

                    att_text = att.fallback.replace(match['replace'],
                                                    link.format(**match))
                else:
                    match = self.url_pat.search(msg.text)
                    if match:
                        match = match.groupdict()
                        match['title'] = att.fallback
                        att_text = msg.text.replace(match['replace'],
                                                    link.format(**match))
                    else:
                        att_text = att.fallback
                attachment_msg.append(att_text)

        data['msg'] += '<br>'.join(attachment_msg)
        return data


def get_reporter(args, query):
    """Return object of right reporter class"""
    reporters = {'text': TextReporter,
                 'html': StaticHtmlReporter}

    klass = reporters.get(args.format, NoneReporter)
    if klass.__name__ == 'Reporter':
        logging.warning('None, or wrong (%s) formatter selected, falling to'
                        ' None Reporter', args.format)
    return klass(args, query)
