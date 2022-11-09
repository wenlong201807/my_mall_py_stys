from django.shortcuts import render, redirect
from django.views import View
from django import http
import re

from django_redis import get_redis_connection

from .models import User
from django.contrib.auth import login
from meiduo_mall.utils.response_code import RET
from . import constants
from django.db import DatabaseError
from django.urls import reverse


class MobileCountView(View):
    def get(self, request, mobile):
        # 接收
        # 验证
        # 处理：判断手机号是否存在
        count = User.objects.filter(mobile=mobile).count()
        # 响应：提示是否存在
        return http.JsonResponse({
            'count': count,
            'code': RET.OK,
            'errmsg': "OK"
        })


class UsernameCountView(View):
    def get(self, request, username):  # url中的变量 username
        # 接收：通过路由在路径中提取
        # 验证：路由的正则表达式
        # 处理：判断用户名是否存在
        count = User.objects.filter(username=username).count()
        # 响应：提示是否存在
        return http.JsonResponse({
            'count': count,
            'code': RET.OK,
            'errmsg': 'OK'
        })


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 接收
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        password2 = request.POST.get('cpwd')
        mobile = request.POST.get('phone')
        # image_code = request.POST.get('image_code')
        sms_code = request.POST.get('msg_code')
        allow = request.POST.get('allow')

        # 验证
        # 1.非空
        if not all([username, password, password2, mobile, sms_code, allow]):
            return http.HttpResponseForbidden('填写数据不完整')
        # 2.用户名
        if not re.match('^[a-zA-Z0-9_-]{5,20}$', username):
            return render(request, 'register.html', {'error_name_message': '用户名为5-20个字符'})
        if User.objects.filter(username=username).count() > 0:
            return render(request, 'register.html', {'error_name_message': '用户名已经存在'})

        # 密码
        if not re.match('^[0-9A-Za-z]{8,20}$', password):
            return render(request, 'register.html', {'error_password_message': '密码为8-20个字符'})

        # 确认密码
        if password != password2:
            return render(request, 'register.html', {'error_password2_message': '两个密码不一致'})

        # 手机号
        if not re.match('^1[3456789]\d{9}$', mobile):
            return render(request, 'register.html', {'error_phone_message': '手机号错误'})
        if User.objects.filter(mobile=mobile).count() > 0:
            return render(request, 'register.html', {'error_phone_message': '手机号存在'})

        # 短信验证码
        # 1.读取redis中的短信验证码
        redis_cli = get_redis_connection('sms_code')  # 对应到settings 中redis桶的约定
        sms_code_redis = redis_cli.get('sms_%s' % mobile)
        sms_code_redis = sms_code_redis.decode('utf-8', 'ignore')
        # 2.判断是否过期
        if sms_code_redis is None:
            return render(request, 'register.html', {'error_sms_code_message': '短信验证码已经过期'})
        # 3.删除短信验证码，不可以使用第二次
        redis_cli.delete('sms_%s' % mobile)
        # redis_cli.delete(mobile + '_flag')
        # 4.判断是否正确
        if sms_code_redis.lower() != sms_code.lower():
            return render(request, 'register.html', {'error_sms_code_message': '输入的短信验证码错误'})

        # 是否勾选
        if allow != 'on':
            return render(request, 'register.html', {'error_allow_message': '请勾选用户协议'})

        # 处理
        # 1.创建用户对象

        # 保存注册数据, 是注册业务的核心
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
