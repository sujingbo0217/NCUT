# -*- coding = utf-8 -*-
# @Time : 2023/5/28 10:39 AM
# @Author : Jingbo Su
# @File : client.py
# @Software : PyCharm

import socket
import threading

from src.constant import *
from utils.error import Disconnection
from utils.receive import serialize
from utils.output import message
from utils.send import send_message


class Client(threading.Thread):
    def __init__(self, addr, port, user_list_gui, user_list, output_box, username):
        threading.Thread.__init__(self)
        self.addr = addr
        self.port = port
        self.user_list_gui = user_list_gui
        self.user_list = user_list
        self.output_box = output_box
        self.username = username
        self.client_socket = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.addr, self.port))
        self.stop_flag = False
        self.ok = True

    def run(self):
        while not self.stop_flag:
            # Verify username
            if self.ok:
                self.verify()

            # Socket communication
            try:
                msg = serialize(self.sock.recv(1024))
                proto = msg.get('protocol')
                data = msg.get('data')
                if proto == CHAT_EXIT:
                    break
                elif proto == USER_LIST:
                    self.user_list = msg.get('data')
                    self.user_list_gui.set(self.user_list)
                elif proto == CHAT_CONTENT:
                    message(self.output_box, msg.get('data'))
                elif proto == PRIVATE_CHAT:
                    # Server -> Client
                    split_str = data.split(':')
                    username = split_str[-1].strip('@').strip()
                    user_msg = ''.join(split_str[1:-1]).strip()
                    message(self.output_box, f'[{username}@You]: {user_msg}')
                else:
                    pass
            except Disconnection('Server Offline'):
                pass
        message(self.output_box, 'Server Offline')
        self.stop_client()

    def verify(self):
        while True:
            if self.ok:
                username_data = {
                    'protocol': USER_NAME,
                    'data': self.username,
                }
                send_message(self.sock, username_data)
                self.ok = False
            response = serialize(self.sock.recv(1024))
            if response.get('protocol') == USED_NAME:
                err = f'[System]: {self.username} already exists, please select another one'
                message(self.output_box, err)
                self.ok = True
            elif response.get('protocol') == USER_LIST:
                self.user_list = response.get('data')
                self.user_list_gui.set(self.user_list)
                break
            else:
                pass

    def stop_client(self):
        self.sock.close()
        self.stop_flag = True
