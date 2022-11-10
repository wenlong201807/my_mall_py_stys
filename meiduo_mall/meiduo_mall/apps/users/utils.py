# 自定义用户认证的后端: 实现多账号登录
from django.contrib.auth.backends import ModelBackend
import re

from .models import User


def get_user_by_account(account):
    """
    通过账号获取用户
    :param account 用户名或者手机号
    :return user
    """
    try:
        # 校验username 参数是用户名还是手机号
        if re.match(r'^1[3-9]\d{9}$', account):
            # account == 手机号
            user = User.objects.get(mobile=account)
        else:
            # account == 用户名
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


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
        # 使用账号查询用户
        user = get_user_by_account(username)

        # 如果可以查到用户，还需要校验密码是否正确
        if user and user.check_password(password):
            # 返回user
            return user
        else:
            return None
