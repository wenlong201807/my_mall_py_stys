# 自定义用户认证的后端: 实现多账号登录
from django.contrib.auth.backends import ModelBackend


class UsernameMobilBackend(ModelBackend):
    """
    自定义用户认证后端-重写与扩展父类
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        重写用户认证的方法
        1 使用账号查询用户[难点] username(可能是用户名或者手机号)
        2 如果可以查询到用户，需要校验密码是否正确
        3 返回user
        """