#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import select
from json import dumps, loads


class ChatClient:
    def __init__(self, port=8888, render_message=None, get_nickname=None):
        self.render_message = render_message
        self.get_nickname = get_nickname
        self.nickname = self.get_nickname()
        self.port = port
        # connecting to server
        try:
            self.sock_to_read = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock_to_read.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock_to_read.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.sock_to_read.bind(('0.0.0.0', port))

            self.sock_to_write = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock_to_write.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        except Exception as e:
            raise ConnectionError('Unable to connect')

    def send_request(self, sock_to_write, action, data=None):
        object_to_send = {'action': action, 'data': data, 'nickname': self.nickname}
        sock_to_write.sendto(bytes(dumps(object_to_send), 'UTF-8'), ('255.255.255.255', self.port))

    def iterate(self):
        socket_list = [self.sock_to_read]
        ready_to_read, _, _ = select.select(socket_list, [], [], 0)

        for sock in ready_to_read:
            # incoming message from server
            if sock == self.sock_to_read:
                data = sock.recv(4096).decode('utf-8')
                if not data:
                    raise ConnectionAbortedError('Disconnected from chat server')
                else:
                    self.render_message(data)

    def send_message(self, message):
        self.send_request(self.sock_to_write, 'message', message)


if __name__ == "__main__":
    pass
