# -*- coding = utf-8 -*-
# @Time : 2023/5/23 6:45 PM
# @Author : Jingbo Su
# @File : urls.py
# @Software : PyCharm

from django.urls import path

from .views import *

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'user_register'}), name='user'),
    path('login/', UserViewSet.as_view({'post': 'user_login'}), name='user'),

    path('upload_server/', ImageViewsSet.as_view({'post': 'upload_server'}), name='mnist'),
    path('upload/', ImageViewsSet.as_view({'post': 'upload'}), name='mnist'),
    path('download/', ImageViewsSet.as_view({'post': 'download'}), name='mnist'),
    path('predict/', ImageViewsSet.as_view({'post': 'predict'}), name='mnist'),
    path('delete/', ImageViewsSet.as_view({'post': 'delete'}), name='mnist'),
]
