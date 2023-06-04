# -*- coding = utf-8 -*-
# @Time : 2023/5/30 12:37 PM
# @Author : Jingbo Su
# @File : sock.py
# @Software : PyCharm

import threading

from src.constant import *
from utils.output import message
from utils.receive import serialize
from utils.send import broadcast, send_message
from utils.error import Disconnection, UserNotExists


class Socket(threading.Thread):
    def __init__(self, conn, addr, client_thread, client_socket, user_list_gui, user_list, output_box, username):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.client_thread = client_thread
        self.client_socket = client_socket
        self.user_list_gui = user_list_gui
        self.user_list = user_list
        self.output_box = output_box
        self.username = username

    def run(self):
        while True:
            # Receive messages from client
            recv = serialize(self.conn.recv(1024))
            if recv is None:
                continue

            proto = recv.get('protocol')
            data = recv.get('data')

            if proto == CHAT_EXIT:
                break
            elif proto == CHAT_CONTENT:
                new_msg = f'[{self.username}]: {data}'
                message(self.output_box, new_msg)
                new_data = {
                    'protocol': CHAT_CONTENT,
                    'data': new_msg,
                }
                broadcast(self.client_socket, new_data, [self.username])
            elif proto == PRIVATE_CHAT:
                username = data.split(':')[0].strip('@').strip()
                if username in self.client_socket:
                    # Send private message to client with username
                    send_message(self.client_socket.get(username), recv)
                else:
                    raise UserNotExists('User Not Exists')
            else:
                pass

        # Client exits
        try:
            common_msg = {
                'protocol': CHAT_CONTENT,
                'data': f'\'{self.username}\' has exited the chat room.',
            }
            exit_msg = {
                'protocol': CHAT_CONTENT,
                'data': f'You have exited the chat room.',
            }
            user_list = {
                'protocol': USER_LIST,
                'data': self.user_list,
            }
            message(self.output_box, f'\'{self.username}\' has exited the chat room.')
            broadcast(self.client_socket, user_list, [self.username])
            broadcast(self.client_socket, common_msg, [self.username])
            send_message(self.conn, exit_msg)
            self.conn.close()
        except Disconnection('Client Offline'):
            pass
