from django.shortcuts import render
from django.views import View
from meiduo_mall.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from . import constants
from django import http


class ImageCodeView(View):
    def get(self, request, uuid):
        # 1 接收和校验参数
        # 2 实现主体业务逻辑: 生成，保存，响应图形验证码
        # 3 响应结果

        # 1.生成图片的文本、数据
        text, code, image = captcha.generate_captcha()
        print(text, code)  # VEMZ6bU3x9agGOilpWR85qIK PFMN

        # 2.保存图片文本，用于后续与用户输入值对比
        redis_cli = get_redis_connection('verify_code')  # settings中配置的图形码对应到redis桶中
        # redis_cli.setex('key', 'expires', 'value')
        redis_cli.setex('img_%s' % uuid, constants.IMAGE_CODE_EXPIRES, code)

        # 指南 setex -> https://www.runoob.com/redis/strings-setex.html
        # redis手册 http://doc.redisfans.com/

        # 3 响应：输出图片数据
        return http.HttpResponse(image, content_type='image/jpg')
