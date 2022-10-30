from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^authorizations/$', obtain_jwt_token),  # 内部对 用户名和密码做了校验

]