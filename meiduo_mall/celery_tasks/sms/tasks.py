# 定义任务
from celery_tasks.main import celery_app
from celery_tasks.sms.yuntongxun.ccp_sms import CCP
from . import constants


# 使用装饰器装饰异步任务，保证celery识别任务 name 为别名，后续直接调用时使用
@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    """
    发送短信验证码的异步任务

    """
    send_ret = CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_EXPIRES // 60], 1)
    return send_ret
