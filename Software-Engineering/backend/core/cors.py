# -*- coding = utf-8 -*-
# @Time : 2023/6/5 9:21 PM
# @Author : Jingbo Su
# @File : cors.py
# @Software : PyCharm

from django.utils.deprecation import MiddlewareMixin

class Cors(MiddlewareMixin):
    def process_response(self, request, response):
        response['Access-Control-Allow-Headers'] = '*'
        response['Access-Control-Allow-Origin'] = '*'
        return response
