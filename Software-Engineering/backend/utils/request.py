# -*- coding = utf-8 -*-
# @Time : 2023/6/3 9:25 PM
# @Author : Jingbo Su
# @File : request.py
# @Software : PyCharm

from rest_framework.request import Request
from drf_yasg import openapi

methods = [
    openapi.IN_HEADER,
    openapi.IN_QUERY,
    openapi.IN_BODY,
]

def get_request(request: Request, method: str):
    if method not in methods:
        raise Exception("Invalid method")
    if method == openapi.IN_HEADER or method == openapi.IN_QUERY:
        return request.query_params
    # openapi.IN_BODY
    return request.data

def get_image(request: Request, file_name: str):
    image = request.FILES.get(file_name)
    name = image.name
    return name, image
