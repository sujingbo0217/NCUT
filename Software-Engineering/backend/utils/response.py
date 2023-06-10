# -*- coding = utf-8 -*-
# @Time : 2023/6/2 1:48 AM
# @Author : Jingbo Su
# @File : response.py
# @Software : PyCharm

from rest_framework.response import Response


class APIResponse(Response):
    def __init__(self, data=None, error=None, user=None,
                 status=None, template_name=None, headers=None, exception=False, content_type=None, **kwargs):
        dic = {
            'content': {}
        }

        if status is not None:
            dic['result_code'] = status

        if error is not None:
            dic['error'] = error

        if data is not None:
            dic['content']['record'] = data

        if user is not None:
            dic['content']['user'] = user

        if kwargs is not None:  # Custom params
            dic.update(kwargs)

        super().__init__(data=dic, status=status,
                         template_name=template_name, headers=headers,
                         exception=exception, content_type=content_type)