from django.contrib.auth.mixins import LoginRequiredMixin
from django import http
from .response_code import RET


class LoginRequiredJSONMixin(LoginRequiredMixin):
    """自定义判断用户是否登录的扩展类，返回json"""

    # 为什么需要重写handle_no_permission?
    # 因为判断用户是否登录的操作，父类已经完成子类，只需要关心，如果用户未登录，对应怎样的操作
    def handle_no_permission(self):
        """直接响应json数据"""
        return http.JsonResponse({'cod': RET.SESSIONERR, 'errmsg': '用户未登录'})