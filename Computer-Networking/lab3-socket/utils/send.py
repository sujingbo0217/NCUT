# -*- coding = utf-8 -*-
# @Time : 2023/5/30 4:46 PM
# @Author : Jingbo Su
# @File : send.py
# @Software : PyCharm

import json
import socket

from utils.error import Disconnection
from src.constant import SUCCESS, FAILED


def send_message(sock: socket, msg: object) -> bool:
    """
    :param sock: socket
    :param msg: json message
    :return: bool
    """""
    data = json.dumps(msg).encode('utf-8')
    try:
        sock.send(data)
        return SUCCESS
    except Disconnection('Client Offline'):
        return FAILED


def broadcast(client_socket: dict, data: object, exclude=None):
    """
    :param client_socket: All client connections
    :param data: Info passed from server
    :param exclude: Excluding user list
    :return:
    """
    data = json.dumps(data, ensure_ascii=False)
    try:
        for username, conn in client_socket.items():
            if exclude is None or username not in exclude:
                try:
                    conn.send(data.encode('utf-8'))
                except Exception as e:
                    # Handle specific disconnection error or log the error
                    print(f"Error sending data to {username}: {e}")
        return SUCCESS
    except Exception as e:
        # Handle broadcast error or log the error
        print(f"Error during broadcast: {e}")
        return FAILED
