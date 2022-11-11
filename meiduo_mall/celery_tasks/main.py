# celery 入口
from celery import Celery
import os

# 读取django项目的配置
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ["DJANGO_SETTINGS_MODULE"] = "meiduo_mall.settings.dev"  # 与django进程独立，需要添加启动配置

# 创建celery对象
celery_app = Celery('meiduo')

# 加载配置
celery_app.config_from_object('celery_tasks.config')

# 加载可用的任务[注册任务]
celery_app.autodiscover_tasks([
    'celery_tasks.sms',
    'celery_tasks.email',  # 任务文件夹名字
])

# 启动命令
"""
[有虚拟环境的]终端下执行:
cd meiduo_mall
-> 子目录包含 celery_tasks

执行celery命令
$ celery -A celery_tasks.main worker -l info
"""