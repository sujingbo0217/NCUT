# -*- coding = utf-8 -*-
# @Time : 2023/5/29 10:39 AM
# @Author : Jingbo Su
# @File : lex.py
# @Software : PyCharm

from src.constant import *
from utils.error import LexicalError

def lex(expr: str) -> str:
    # Split words by spaces according to operators
    for _o in O:
        if _o in expr:
            expr = expr.replace(_o, f' {_o} ')

    # Split words by spaces according to delimiters
    for de in D:
        expr = expr.replace(de, f' {de} ')

    _expr = expr.split()

    ret = '#'
    is_label = False
    for word in _expr:
        if is_label:
            ret += 'err'
            is_label = False
        else:
            if word.isdigit():
                ret += 'i'
            elif word in K:
                ret += 'err'
                if word == 'GOTO':
                    is_label = True
            elif word in O:
                ret += word
            elif word in D:
                ret += word
            elif word[-1] == ':':
                ret += 'err'
            elif word.isalpha():
                ret += 'i'
            else:
                raise LexicalError('Invalid token')
    ret += '#'
    return ret