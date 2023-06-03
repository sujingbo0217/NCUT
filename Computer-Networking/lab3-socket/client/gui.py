# -*- coding = utf-8 -*-
# @Time : 2023/6/1 6:15 PM
# @Author : Jingbo Su
# @File : gui.py
# @Software : PyCharm

import sys
import tkinter as tk
from tkinter import messagebox

from client import Client
from src.constant import *
from utils.output import message
from utils.send import send_message
from utils.error import Disconnection


class GUI:
    def __init__(self):
        self.cli = None
        self.user_list = []
        self.namelist = []
        self.t = None

        # Window title
        self.root = tk.Tk()
        self.root.title('Socket Client')

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
        self.ip_input = tk.Entry(self.top_frame, textvariable=self.ip_addr, width=12)
        self.ip_input.pack(fill=tk.X, side=tk.LEFT)
        self.port_input = tk.Entry(self.top_frame, textvariable=self.port, width=5)
        self.port_input.pack(side=tk.LEFT)

        self.start_btn = tk.Button(self.top_frame, text="Start", width=16, command=self.start_client)
        self.start_btn.pack(side=tk.LEFT)
        # self.stop_btn = tk.Button(self.top_frame, text="Stop", width=16, command=self.stop_client)
        # self.stop_btn.pack(side=tk.LEFT)

        # Information frame
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(fill=tk.BOTH, expand=True)

        # User list
        self.users = tk.StringVar()
        self.user_list_box = tk.Listbox(self.info_frame, listvariable=self.users, width=20, selectmode=tk.EXTENDED)
        self.user_list_box.bind('<ButtonRelease-1>', self.private_chat)
        self.user_list_box.pack(fill=tk.Y, side=tk.LEFT)

        # Message text
        self.message_bar = tk.Scrollbar(self.info_frame)
        self.message_bar.pack(fill=tk.Y, side=tk.LEFT)
        self.output_box = tk.Text(self.info_frame, width=80, font=("Symbol", 14), yscrollcommand=self.message_bar.set)
        self.output_box.pack(fill=tk.Y, side=tk.RIGHT)   # expand=True

        # Chat frame
        self.chat_frame = tk.LabelFrame(self.root, text="Chat", padx=5, pady=5)
        self.chat_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Client down bar (chat content)
        self.down_frame = tk.Frame(self.chat_frame)
        self.down_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Username entry box and create button
        self.username_frame = tk.Frame(self.down_frame)
        self.username_frame.pack(fill=tk.X, side=tk.TOP)

        self.username_label = tk.Label(self.username_frame, text="Username:")
        self.username_label.pack(side=tk.LEFT)

        self.username = tk.StringVar()
        self.username_box = tk.Entry(self.username_frame, textvariable=self.username, width=32)
        self.username_box.pack(side=tk.LEFT)

        # Chat content entry box and send button
        self.chat_content_frame = tk.Frame(self.down_frame)
        self.chat_content_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.chat_content_label = tk.Label(self.chat_content_frame, text="Chat:")
        self.chat_content_label.pack(side=tk.LEFT)

        self.chat_content = tk.StringVar()
        self.send_box = tk.Entry(self.chat_content_frame, textvariable=self.chat_content, width=32)
        self.send_box.pack(side=tk.LEFT)

        self.send_btn = tk.Button(self.chat_content_frame, text="Send", width=12, command=self.send_message)
        self.send_btn.pack(side=tk.LEFT)

        # Disconnect socket and stop the threads
        self.root.protocol('WM_DELETE_WINDOW', self.close_window)
        self.root.mainloop()

    def send_username(self):
        uname = self.username_box.get()
        data = {
            'protocol': USER_NAME,
            'data': uname,
        }
        if self.cli is not None:
            try:
                send_message(self.cli.sock, data)
                message(self.output_box, f'You have entered the chat room')
            except Exception as e:
                raise e
        messagebox.showwarning('Warning', 'Please connect to the server first')

    def start_client(self):
        username = self.username.get()
        if username != '':
            try:
                self.cli = Client(self.ip_addr.get(), self.port.get(),
                                  self.users, self.user_list, self.output_box, username)
                self.cli.setDaemon(True)  # Must be set before start() is called, otherwise RuntimeError is raised
                self.cli.start()
                message(self.output_box, '=== Client Started Successfully ===')
            except Exception as e:
                messagebox.showwarning('Error', f'{e}')
                raise Disconnection('Server Offline')
        else:
            messagebox.showwarning('Warning', 'Please fill username first!')

    def stop_client(self):
        pass

    def send_message(self):
        if self.cli is not None:
            msg = self.send_box.get()
            data = {
                'protocol': CHAT_CONTENT,
                'data': msg,
            }
            send_message(self.cli.sock, data)
            self.send_box.delete(0, tk.END)
            message(self.output_box, f'[You]: {msg}')
        else:
            messagebox.showwarning('Warning', 'Please connect to the server first')

    def private_chat(self, e):
        msg = None
        target = None
        indices = self.user_list_box.curselection()
        print(e)

        if indices is not None:
            for k in indices:
                target = self.user_list_box.get(k)
                self.chat_content.set(f'@{target}: ')
                msg = self.send_box.get()

        if self.cli is not None and target is not None:
            if self.cli.client_socket is None:
                # Send private chat request to server Client -> Server
                self.cli.send_private_chat_request(target, msg)
            else:
                # Send private chat message to client: Client <-> Client
                self.cli.send_private_chat_message(target, msg)

    def close_window(self):
        if self.cli is not None:
            data = {
                'protocol': CHAT_EXIT,
                'data': '',
            }
            send_message(self.cli.sock, data)
        self.root.destroy()
        sys.exit()
