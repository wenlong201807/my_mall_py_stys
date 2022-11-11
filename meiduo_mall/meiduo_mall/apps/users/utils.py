# 自定义用户认证的后端: 实现多账号登录
from django.contrib.auth.backends import ModelBackend
import re
from django.conf import settings
from itsdangerous import URLSafeSerializer

from .models import User
from . import constants

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = '1573511441@qq.com@qq.com'  # 填写发信人的邮箱账号
my_pass = '666777'  # 发件人邮箱授权码


# my_user = '@qq.com'  # 收件人邮箱账号


def send_mail(to_email):  # 发送邮件失败
    ret = True
    try:
        msg = MIMEText('this is just a test', 'plain', 'utf-8')  # 填写邮件内容
        msg['From'] = formataddr(["tracy", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["test", to_email])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "发送邮件测试"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱授权码
        server.sendmail(my_sender, [to_email, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret


def generate_verfy_email_url(user):  # 失败 10-11
    """商城激活链接"""
    s = URLSafeSerializer(settings.SECRET_KEY, 'auth')
    data = {
        'user_id': user.id,
        'email': user.email
    }
    token = s.dumps(data)
    print(token)
    # http://www.meiduo.site:8000/emails/verification/?token=${token}
    return settings.EMAIL_VERIFY_URL + token()


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
