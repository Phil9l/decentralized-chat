#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import select
import sys
import signal
from json import loads
from optparse import OptionParser
from client import ChatClient


class ConsoleChat:
    def __init__(self, port=8888):
        self.chat = ChatClient(port, self.render_message, self.get_nickname)

    def iterate(self):
        self.chat.iterate()
        data = self.get_input()
        if data is not None:
            self.chat.send_message(data)

    @staticmethod
    def render_message(message):
        sys.stdout.write('\r')
        message = loads(message)
        sys.stdout.write('{}: {}\n'.format(message['nickname'], message['data']))
        sys.stdout.write('> ')
        sys.stdout.flush()

    @staticmethod
    def get_nickname():
        name = input('[Auth] Enter your nickname\n> ')
        return name

    @staticmethod
    def get_input():
        stdin = [sys.stdin]
        ready_to_read, _, _ = select.select(stdin, [], [], 0)
        if len(ready_to_read) == 0:
            return None
        message = sys.stdin.readline()
        sys.stdout.write('\x1b[1A\r> ')
        sys.stdout.flush()
        return message


def signal_handler(signal, frame):
    print('\rYou left chat manually by pressing Ctrl + C')
    sys.exit(0)


def get_options():
    parser = OptionParser(usage='usage: %prog [options] hostname')
    parser.add_option(
        '-p', '--port', dest='port', help='Run server on given port',
        type='int', metavar='PORT', default=8888
    )
    (opt, args) = parser.parse_args()
    return opt, args


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    (options, args) = get_options()
    console_chat = ConsoleChat(options.port)
    while True:
        console_chat.iterate()
