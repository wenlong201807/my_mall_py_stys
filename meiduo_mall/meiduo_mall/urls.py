"""meiduo_admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

urlpatterns = [
    url('^meiduo_admin/', include('meiduo_admin.urls')),
    url(r'^', include(('users.urls', 'users'), namespace='users')),  # 增加命名空间
    url(r'^', include(('contents.urls', 'contents'), namespace='contents')),
    url('^', include('verifycations.urls')),  # 校验模块
    url('^', include('oauth.urls')),  # 第三方授权模块
]
