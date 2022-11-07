from django.conf.urls import url
from . import views

urlpatterns = [
    # 首页广告 '/'
    url('^$', views.IndexView.as_view(), name='index'),
]
