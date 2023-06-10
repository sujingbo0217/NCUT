# -*- coding = utf-8 -*-
# @Time : 2023/5/5 4:30 PM
# @Author : Jingbo Su
# @File : serializers.py
# @Software : PyCharm

from rest_framework import serializers
from .models import Users, Images


class UserSerializer(serializers.Serializer):
    class Meta:
        model = Users
        fields = '__all__'

    def create(self, validated_data):
        user = Users.objects.create(username=validated_data['username'],
                                    password=validated_data['password'])
        user.save()
        return user


class ImageSerializer(serializers.Serializer):
    class Meta:
        model = Images
        fields = '__all__'

    def create(self, validated_data):
        image = Images.objects.create(
            userId=validated_data['userId'],
            image=validated_data['image'], name=validated_data['name'],
            label=validated_data['label'], pred=validated_data['pred'],
            prob=validated_data['prob'], result=validated_data['result']
        )
        image.save()
        return image
