from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django import http
from django.contrib.auth import login, authenticate, logout
import re
import json
import logging
from django_redis import get_redis_connection
from django.db import DatabaseError
from django.urls import reverse

from django.conf import settings
from .models import User
from meiduo_mall.utils.response_code import RET
from .utils import generate_verfy_email_url, send_mail
from meiduo_mall.utils.my_loginview import LoginRequiredJSONMixin  # 重写父类，判断用户是否是登录态
from celery_tasks.email.tasks import send_verify_mail

# 创建日志输出器
logger = logging.getLogger('django')


class EmailView(LoginRequiredJSONMixin, View):
    """添加邮箱号"""

    # LoginRequiredJSONMixin 判断是否登录，这里没要再写里，因为系统未登录，是进不来这里的

    def put(self, request):
        # 接收参数
        json_dict = json.loads(request.body.decode())  # body 是 byte类型。注意此处数据类型转换
        email = json_dict.get('email')

        # 验证参数合法性
        if not all([email]):  # 邮箱号是否为空
            return http.JsonResponse({'code': RET.EMAILERR, 'errmsg': "邮箱无效"})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.JsonResponse({'code': RET.EMAILERR, 'errmsg': "邮箱格式错误"})

        # 处理：修改当前登录用户的邮箱属性,保存到数据库中
        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RET.DBERR, 'errmsg': "添加邮箱失败"})

        # 发邮件：耗时代码，使用celery异步
        # send_mail('美多商城-邮箱激活','',settings.EMAIL_FROM,[email],html_message='')
        # 将用户编号加密
        # token = meiduo_signature.dumps({'user_id': request.user.id}, constants.EMAIL_ACTIVE_EXPIRES)
        # 拼接激活的链接地址
        # verify_url = settings.EMAIL_VERIFY_URL + '?token=' + token
        verify_url = generate_verfy_email_url(request.user)
        # 异步发邮件
        send_verify_mail.delay(email, verify_url)
        # send_mail(email)  # fail
        # 响应
        return http.JsonResponse({'code': RET.OK, 'errmsg': "OK"})


class UserInfoView(LoginRequiredMixin, View):
    """
    用户中心
    LoginRequiredMixin 继承功能: 如果没有登录，则先跳转到登录页，登录成功后，再进入此页
    """

    def get(self, request):
        # 用户中心页面，有些用户个人信息需要在页面展示，特此收集并返回给页面端
        # 可以进入用户中心，必定是已经登录状态，在request.user中就有user信息
        context = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active,
        }
        return render(request, 'user_center_info.html', context)


class LogoutView(View):
    """用户退出登录"""

    def get(self, request):
        """实现用户退出登录逻辑"""
        # 清除状态保持信息
        logout(request)

        # 退出登录
        response = redirect(reverse('contents:index'))
        # 删除cookie中username
        response.delete_cookie('username')

        # 响应结果：重定向到首页
        return response


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        """
        1 接收参数
        2 校验参数
        3 认证用户
        4 状态保持
        5 响应结果
        """
        # 接收
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        remembered = request.POST.get('remembered')

        # 1.非空
        if not all([username, pwd]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 2.用户名
        if not re.match('^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('输入正确的用户名')

        # 密码
        if not re.match('^[0-9A-Za-z]{8,20}$', pwd):
            return http.HttpResponseForbidden('密码最少8位，最多20位')

        # 验证：根据用户名查询，找到对象后再对比密码
        '''
        user=User.objects.get(username=username)
        user.password==加密(pwd)===>user.check_password(pwd)
        '''
        user = authenticate(request, username=username, password=pwd)
        if user is None:
            # 用户名或密码错误 -> 给爬虫看的
            return render(request, 'login.html', {'account_message': '账号或密码错误'})

        # 保持状态
        login(request, user)
        # 使用remembered 确定状态保持周期(实现记住登录)
        if remembered != 'on':  # 这里为什么是 on作为判断标准呢？
            # 没有记住登录： 状态保持在浏览器会话结束后就销毁
            request.session.set_expiry(0)  # 单位是秒
        else:
            # 记住登录: 状态保持周期为两周(默认是两周)
            request.session.set_expiry(None)

        # 响应结果：
        # 判断路由中是否有next参数，如果有，则跳转到指定页，否则进入首页
        next = request.GET.get('next')
        if next:
            # 重定向到next页
            response = redirect(next)
        else:
            # 默认跳转到首页
            response = redirect(reverse('contents:index'))

        # 为了实现在首页右上角展示用户名信息，需要将用户名缓存到cookie中
        # response.set_cookie('key', 'val', 'expiry')
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)

        # 响应结果: 重定向到首页
        return response


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

        # 响应结果：重定向到首页
        response = redirect(reverse('contents:index'))

        # 为了实现在首页右上角展示用户名信息，需要将用户名缓存到cookie中
        # response.set_cookie('key', 'val', 'expiry')
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)

        # 响应结果: 重定向到首页
        return response
