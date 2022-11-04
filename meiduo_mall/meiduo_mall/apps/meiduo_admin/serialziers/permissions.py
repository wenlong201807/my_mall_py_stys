from rest_framework import serializers
from django.contrib.auth.models import Permission, ContentType


class PerssionsSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Permission  # django 框架自带的权限model，有对应的表
        fields = '__all__'


class ContentTypeSerialzier(serializers.ModelSerializer):
    """
        权限类型序列化器
    """
    # 对应模型表中没有定义name 但是 __str__ 有name字段，就可以直接使用
    name = serializers.CharField(read_only=True)  # read_only=True 只返回前端的数据

    class Meta:
        model = ContentType  # 指定根据那个模型类生成序列化字段
        fields = '__all__'  # 指定生成哪些字段
