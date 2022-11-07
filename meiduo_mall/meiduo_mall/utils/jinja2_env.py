from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment

"""
1 创建环境对象
2 自定义语法 {{ static('静态文件相对路径') }} {{ url('路由的命名空间') }}
3 返回环境对象
"""


def jinja2_environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,  # 获取静态文件的前缀
        'url': reverse,  # 反向解析
    })
    return env


"""
确保可以使用Django模板引擎中的{% url('') %} {% static('') %}这类的语句
"""
