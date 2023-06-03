# -*- coding = utf-8 -*-
# @Time : 2023/5/30 12:30 AM
# @Author : Jingbo Su
# @File : gui.py
# @Software : PyCharm

import sys
import tkinter as tk

from server import Server
from src.constant import *
from utils.output import message
from utils.send import broadcast


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.server = None

        # Window title
        self.root.title('Socket Server')

        # Settings frame
        self.settings_frame = tk.LabelFrame(self.root, text="Settings", padx=5, pady=5)
        self.settings_frame.pack(fill=tk.X, side=tk.TOP)

        # Server top bar (host, port) with buttons
        self.top_frame = tk.Frame(self.settings_frame)
        self.top_frame.pack(fill=tk.X, side=tk.TOP)
        self.ip_addr = tk.StringVar()
        self.ip_addr.set('127.0.0.1')
        self.port = tk.IntVar()
        self.port.set(6666)

        # Entry widget which allows displaying simple text
        self.ip_input = tk.Entry(self.top_frame, textvariable=self.ip_addr, width=12, state=tk.DISABLED)
        self.ip_input.pack(fill=tk.X, side=tk.LEFT)
        self.port_input = tk.Entry(self.top_frame, textvariable=self.port, width=5)
        self.port_input.pack(side=tk.LEFT)

        self.start_btn = tk.Button(self.top_frame, text="Start", width=16, command=self.start_server)
        self.start_btn.pack(side=tk.LEFT)
        # self.stop_btn = tk.Button(self.top_frame, text="Stop", width=16, command=self.stop_server)
        # self.stop_btn.pack(side=tk.LEFT)

        # Information frame
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(fill=tk.BOTH, expand=True)

        # User list
        self.users = tk.StringVar()

        # Message text
        self.message_bar = tk.Scrollbar(self.info_frame)
        self.message_bar.pack(fill=tk.Y, side=tk.LEFT)
        self.output_box = tk.Text(self.info_frame, width=80, font=("Symbol", 14), yscrollcommand=self.message_bar.set)
        self.output_box.pack(fill=tk.BOTH, expand=True)

        # Chat frame
        self.chat_frame = tk.LabelFrame(self.root, text="Chat", padx=5, pady=5)
        self.chat_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Server down bar (chat content)
        self.down_frame = tk.Frame(self.chat_frame)
        self.down_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.chat_content = tk.StringVar()
        self.send_box = tk.Entry(self.down_frame, textvariable=self.chat_content, width=40)
        self.send_box.pack(fill=tk.X, side=tk.LEFT)
        self.send_btn = tk.Button(self.down_frame, text="Send", width=18, command=self.send_message)
        self.send_btn.pack(side=tk.LEFT)

        # Disconnect socket and stop the threads
        self.root.protocol('WM_DELETE_WINDOW', self.close_window)
        self.root.mainloop()

    def start_server(self):
        self.server = Server(self.ip_addr.get(), self.port.get(), self.users, self.output_box)
        self.server.setDaemon(True)  # This must be set before start() is called, otherwise RuntimeError is raised
        self.server.start()
        message(self.output_box, '=== Server Started Successfully ===')

    def stop_server(self):
        if self.server is not None:
            if not self.server.stop_flag:
                empty_user_list = {
                    'protocol': USER_LIST,
                    'data': [],
                }
                broadcast(self.server.client_socket, empty_user_list)

                data = {
                    'protocol': CHAT_CONTENT,
                    'data': 'Server is shutting down...',
                }
                broadcast(self.server.client_socket, data)

                for username, conn in self.server.client_socket.items():
                    conn.close()
                    # self.server.client_thread[username].stop()
                self.server.stop()
                message(self.output_box, '=== Server Stopped ===')

    def send_message(self):
        if self.server is not None:
            msg = f'[Admin]: {self.chat_content.get()}'
            data = {
                'protocol': CHAT_CONTENT,
                'data': msg,
            }
            broadcast(self.server.client_socket, data)
            self.send_box.delete(0, tk.END)
            message(self.output_box, msg)

    def close_window(self):
        self.stop_server()
        self.root.destroy()
        sys.exit()
