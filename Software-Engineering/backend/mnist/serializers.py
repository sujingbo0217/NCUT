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
            image=validated_data['image'], name=validated_data['name'],
            label=validated_data['label'], pred=validated_data['pred'],
            prob=validated_data['prob'], result=validated_data['result']
        )
        image.save()
        return image


class ImageInfoSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=64)
    url = serializers.SerializerMethodField()
    label = serializers.CharField(max_length=4)  # User give
    pred = serializers.CharField(max_length=4)  # Predicted by mlp
    prob = serializers.CharField(max_length=8)  # Predict probability
    result = serializers.BooleanField()  # Diff between real label and predict result

    def get_url(self, obj):
        return obj.image.url
