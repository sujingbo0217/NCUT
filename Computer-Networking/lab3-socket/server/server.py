# -*- coding = utf-8 -*-
# @Time : 2023/5/30 12:52 PM
# @Author : Jingbo Su
# @File : run.py
# @Software : PyCharm

import socket
import threading

from sock import Socket
from src.constant import *
from utils.output import message
from utils.receive import serialize
from utils.send import send_message, broadcast


class Server(threading.Thread):
    def __init__(self, addr, port, user_list_gui, output_box):
        threading.Thread.__init__(self)
        self.addr = addr
        self.port = port
        self.user_list_gui = user_list_gui
        self.user_list = []
        self.output_box = output_box
        self.client_thread = {}  # {username: thread}
        self.client_socket = {}  # {username: conn}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket
        self.sock.bind((self.addr, self.port))  # Bind socket
        self.sock.listen(5)  # Max user number
        self.stop_flag = False

    def run(self):
        while not self.stop_flag:
            # Establish new socket connection when a new client comes in
            conn, addr = self.sock.accept()
            sock = Establish(conn, addr, self.client_socket, self.client_thread,
                             self.user_list_gui, self.user_list, self.output_box)
            sock.setDaemon(True)
            sock.start()
            user_num = len(threading.enumerate()) - 2
            if user_num == 1:
                message(self.output_box, '<<1 user online>>')
            else:
                message(self.output_box, f'<<{user_num} users online>>')

        # message(self.output_box, "Server stopped")
        self.sock.close()

    def stop(self):
        self.stop_flag = True


class Establish(threading.Thread):
    def __init__(self, conn, addr, client_socket, client_thread, user_list_gui, user_list, output_box):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.client_socket = client_socket
        self.client_thread = client_thread
        self.user_list_gui = user_list_gui
        self.user_list = user_list
        self.output_box = output_box

    def run(self):
        while True:
            # Verify username
            username_data = serialize(self.conn.recv(1024))
            username = username_data.get('data')
            if username in self.client_socket:
                err = {
                    'protocol': USED_NAME,
                    'data': 'Username already exists',
                }
                send_message(self.conn, err)
            else:
                # Establish socket connection
                self.user_list.append(username)
                self.user_list_gui.set(self.user_list)
                self.client_socket[username] = self.conn
                send_list = {
                    'protocol': USER_LIST,
                    'data': self.user_list,
                }
                broadcast(self.client_socket, send_list, [])
                sock = Socket(self.conn, self.addr, self.client_thread, self.client_socket,
                              self.user_list_gui, self.user_list, self.output_box, username)
                sock.setDaemon(True)
                self.client_thread[username] = sock
                sock.start()
                user_join_msg = f'\'{username}\' has joined the chat room.'
                data = {
                    'protocol': CHAT_CONTENT,
                    'data': user_join_msg,
                }
                # Broadcast to each excluding the sender
                broadcast(self.client_socket, data, [username])
                # Server output
                message(self.output_box, user_join_msg)
                message(self.output_box, '=== Username checked ===')
                break
