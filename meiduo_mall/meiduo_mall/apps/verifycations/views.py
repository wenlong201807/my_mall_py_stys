from django import http
from django.views import View
from django_redis import get_redis_connection

import random
import logging

from meiduo_mall.libs.captcha.captcha import captcha
from meiduo_mall.libs.yuntongxun.ccp_sms import CCP
from meiduo_mall.utils.response_code import RET
from . import constants

# from celery_tasks.sms.tasks import send_sms

# 创建日志输出器
logger = logging.getLogger('django')  # settings 中设置的日志器同名 'django': {  # 定义了一个名为django的日志器


class SMSCCodeView(View):
    def get(self, request, mobile):
        """
        :params mobile url 参数: 手机号
        :return JSON

        业务步骤如下:
        1 接受参数
        2 校验参数

        3 提取图形验证码
        4 删除图形验证码
        5 对比图形验证码

        6 生成短信验证码
        7 保存短信验证码

        8 发送短信验证码

        9 响应结束
        """
        # 1 接受参数
        uuid = request.GET.get('uuid')
        image_code_client = request.GET.get('image_code')

        # 2 校验参数
        if not all([uuid, image_code_client]):  # mobile参数 已经在url中校验完了，不正确，进不来路由
            return http.HttpResponseForbidden({"code": RET.PARAMERR, 'errmsg': '参数不完整'})

        # 3 提取图形验证码
        redis_conn = get_redis_connection('verify_code')
        image_code_server = redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            return http.JsonResponse({'code': RET.IMAGECODEERR, 'errmsg': '图形验证码已失效'})
        # 4 删除图形验证码
        redis_conn.delete('img_%s' % uuid)
        # 5 对比图形验证码
        # python3 中存入redis中的数据类型是bytes ,需要先将bytes转成字符串再比较
        image_code_server = image_code_server.decode("utf-8", "ignore")
        if image_code_server.lower() != image_code_client.lower():  # 优化: 都比较小写字母，不管用户输入的是大下写
            return http.JsonResponse({'code': RET.IMAGECODEERR, 'errmsg': '输入的图形验证码有误'})

        # 6 生成短信验证码： 随机6位数
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info(sms_code)  # 将生成的短信验证码记录到日志器中

        # 7 保存短信验证码
        redis_sms_conn = get_redis_connection('sms_code')
        redis_sms_conn.setex('sms_%s' % mobile, constants.SMS_CODE_EXPIRES, sms_code)
        # 8 发送短信验证码
        # 此处需要整数 //
        CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_EXPIRES // 60], constants.SEND_SMS_TEMPLATE_ID)

        # 9 响应结果
        return http.JsonResponse({'code': RET.OK, 'errmsg': '发送短信成功', 'sms_code': sms_code})

        # 0.是否60秒内
        # if redis_cli_sms.get(mobile + '_flag') is not None:
        #     return http.HttpResponseForbidden({'code': RET.SMSCODERR, 'errmsg': '发送短信太频繁，请稍候再发'})

        # 2.图形验证码是否正确
        # 2.1从redis中读取之前保存的图形验证码文本
        # redis_cli_image = get_redis_connection('image_code')
        # image_code_redis = redis_cli_image.get(uuid)

        # 2.2如果redis中的数据过期则提示
        # if image_code_redis is None:
        #     return http.JsonResponse({'code': RET.IMAGECODEERR, 'errmsg': '图形验证码已过期，点击图片换一个'})
        # # 2.3立即删除redis中图形验证码，表示这个值不能使用第二次
        # redis_cli_image.delete(uuid)
        # # 2.3对比图形验证码：不区分大小写
        # if image_code_redis.decode().lower() != image_code_client.lower():
        #     return http.JsonResponse({'code': RET.IMAGECODEERR, 'errmsg': '图形验证码错误'})

        # 处理
        # 1.生成随机6位数
        # sms_code = '%06d' % random.randint(0, 999999)
        # print(sms_code)
        # # 2.1存入redis
        # redis_cli_sms.setex(mobile, constants.SMS_CODE_EXPIRES, sms_code)
        # # 2.2写发送标记
        # redis_cli_sms.setex(mobile + '_flag', constants.SMS_CODE_FLAG, 1)
        # # 优化：使用管道
        # redis_pl = redis_cli_sms.pipeline()
        # redis_pl.setex(mobile, constants.SMS_CODE_EXPIRES, sms_code)
        # redis_pl.setex(mobile + '_flag', constants.SMS_CODE_FLAG, 1)
        # redis_pl.execute()

        # 3.发短信
        # ccp = CCP()
        # ccp.send_template_sms(mobile, [sms_code, constants.SMS_CODE_EXPIRES / 60], 1)
        # print(sms_code)
        # 通过delay调用，可以将任务加到队列中，交给celery去执行
        # send_sms.delay(mobile, sms_code)


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
