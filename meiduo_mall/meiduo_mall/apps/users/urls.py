from django.conf.urls import url
from . import views

urlpatterns = [
    # 用户注册 添加命名空间 reverse(users:register) == '/register/'
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
    url(r'^mobiles/(?P<mobile>\d+)/count/$', views.MobileCountView.as_view()),
    # url(r'^login/$',views.LoginView.as_view()),
    # url(r'^info/$',views.UserInfoView.as_view()),
    # url(r'^emails/$',views.EmailView.as_view()),
    # url(r'^verify/email/$',views.VerifyEmailView.as_view()),
    # url(r'^addresses/$',views.AddressesView.as_view()),
    # url(r'^addresses/create/$',views.AddressesCreateView.as_view()),
    # url(r'^addresses/(?P<address_id>\d+)/$',views.AddressesUpdateView.as_view()),
    # url(r'^addresses/(?P<address_id>\d+)/default/$',views.AddressesDefaultView.as_view()),
    # url(r'^addresses/(?P<address_id>\d+)/title/$',views.AddressesTitleView.as_view()),
    # url(r'^password/$',views.UserPassWordView.as_view()),
]
