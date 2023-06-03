# -*- coding = utf-8 -*-
# @Time : 2023/5/30 9:44 PM
# @Author : Jingbo Su
# @File : receive.py
# @Software : PyCharm

import json


def serialize(data) -> dict:
    """
    :param data:
    :return: python object
    """
    data = data.decode('utf-8')
    return json.loads(data)
