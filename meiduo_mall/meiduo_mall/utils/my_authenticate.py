from django.contrib.auth.backends import ModelBackend
import re
from users.models import User

#1, 重写系统认证方法
class MyModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
         注意【约定】： 如果是管理员用户 request 无信息，如果是普通用户，request 有信息
        :param request: 请求体
        :param username: 用户名
        :param password: 密码
        :param kwargs: params 参数
        :return: { token, username, id }
        """
        # 0, 判断request对象是否存在
        if request is None:  # 管理员
            try:
                if re.match(r'^1[3-9]\d{9}$',username):
                    user = User.objects.get(mobile=username,is_staff=True)  # is_staff 是管理员，数据表中 is_staff = 1
                else:
                    user = User.objects.get(username=username,is_staff=True)
            except Exception as e:
                return None

            # 2, 校验密码
            if user.check_password(password):
                return user
            else:
                return None

        else:  # 普通用户
            # 1, 根据username查询用户
            try:
                if re.match(r'^1[3-9]\d{9}$',username):
                    user = User.objects.get(mobile=username)
                else:
                    user = User.objects.get(username=username)
            except Exception as e:
                return None

            #2, 校验密码
            if user.check_password(password):
                return user
            else:
                return None