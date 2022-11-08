from django.shortcuts import render, redirect
from django.views import View
from django import http
import re
from .models import User
from django.contrib.auth import login
from . import constants
from django.db import DatabaseError
from django.urls import reverse


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 接收
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        password2 = request.POST.get('cpwd')
        mobile = request.POST.get('phone')
        sms_code = request.POST.get('msg_code')
        allow = request.POST.get('allow')

        # 验证
        # 1.非空
        if not all([username, password, password2, mobile, allow]):
        # if not all([username, password, password2, mobile, sms_code, allow]):
            return http.HttpResponseForbidden('填写数据不完整')
        # 2.用户名
        if not re.match('^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('用户名为5-20个字符')
        if User.objects.filter(username=username).count() > 0:
            return http.HttpResponseForbidden('用户名已经存在')
        # 密码
        if not re.match('^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('密码为8-20个字符')
        # 确认密码
        if password != password2:
            return http.HttpResponseForbidden('两个密码不一致')
        # 手机号
        if not re.match('^1[3456789]\d{9}$', mobile):
            return http.HttpResponseForbidden('手机号错误')
        if User.objects.filter(mobile=mobile).count() > 0:
            return http.HttpResponseForbidden('手机号存在')
        # 是否勾选
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')
        # 短信验证码
        # 1.读取redis中的短信验证码
        # redis_cli = get_redis_connection('sms_code')
        # sms_code_redis = redis_cli.get(mobile)
        # # 2.判断是否过期
        # if sms_code_redis is None:
        #     return http.HttpResponseForbidden('短信验证码已经过期')
        # # 3.删除短信验证码，不可以使用第二次
        # redis_cli.delete(mobile)
        # redis_cli.delete(mobile + '_flag')
        # # 4.判断是否正确
        # if sms_code_redis.decode() != sms_code:
        #     return http.HttpResponseForbidden('短信验证码错误')

        # 处理
        # 1.创建用户对象

        # 保存注册数据, 是注册业务的核心
        # return render(request, 'register.html', {'register_errmsg': '注册失败'})

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                mobile=mobile
            )
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '注册失败'})
        # 2.状态保持
        login(request, user)

        # 向cookie中写用户名，用于客户端显示
        # response = redirect('/')
        # response.set_cookie('username', username, max_age=constants.USERNAME_COOKIE_EXPIRES)

        # 响应结果，重定向到首页
        # return http.HttpResponse('注册成功，重定向到首页')
        # reverse('contents:index') == '/'
        return redirect(reverse('contents:index'))