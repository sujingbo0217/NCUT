# -*- coding = utf-8 -*-
# @Time : 2023/5/30 4:44 PM
# @Author : Jingbo Su
# @File : output.py
# @Software : PyCharm

import tkinter as tk


def message(output_box: tk.Text, msg: str):
    """
    :param output_box: tk.Text()
    :param msg: str
    :return:
    """
    output_box.insert(tk.END, f'{msg}\n\n')  # Insert CHARS(msg) before the characters at INDEX (tk.END)
    output_box.see(tk.END)     # Scroll such that the character at INDEX (tk.END) is visible
