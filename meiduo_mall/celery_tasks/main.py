# celery 入口
from celery import Celery
import os

# 读取django项目的配置
os.environ["DJANGO_SETTINGS_MODULE"] = "meiduo_mall.settings.dev"

# 创建celery对象
celery_app = Celery('meiduo')

# 加载配置
celery_app.config_from_object('celery_tasks.config')

# 加载可用的任务[注册任务]
celery_app.autodiscover_tasks([
    'celery_tasks.sms',
])
