from django import http
from django.conf import settings  # 启动时的配置文件
from django.views import View
from QQLoginTool.QQtool import OAuthQQ
from meiduo_mall.utils.response_code import RET
from users.models import User


class OAuthQQURLView(View):
    def get(self, request):
        next_url = request.GET.get('next')

        # 创建授权对象
        oauthqq = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_CLIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT_URI,
            state=next_url
        )
        # 生成qq登录扫码连接地址
        login_url = oauthqq.get_qq_url()

        # 响应
        return http.JsonResponse({
            'code': RET.OK,
            'errmsg': "OK",
            'login_url': login_url
        })

