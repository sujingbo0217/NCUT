# -*- coding = utf-8 -*-
# @Time : 2023/5/29 8:56 PM
# @Author : Jingbo Su
# @File : get_top.py
# @Software : PyCharm

from lab2.src.constant import A_op

def get_top_vt(stk: list) -> str:
    for st in reversed(stk):
        if st in A_op:
            return st
