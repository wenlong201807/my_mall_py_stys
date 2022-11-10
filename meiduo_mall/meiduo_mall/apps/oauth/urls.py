from django.conf.urls import url
from . import views

urlpatterns = [
    # 提供qq登录扫码的页面地址，否则404
    url('^qq/login/$', views.OAuthQQURLView.as_view()),
    # url('^oauth_callback$', views.OAuthQQOpenidView.as_view()),
]
