from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from meiduo_admin.home import home_views

urlpatterns = [
    url(r'^authorizations/$', obtain_jwt_token),  # 内部对 用户名和密码做了校验
    url(r'^statistical/total_count/$', home_views.UserTotalCountView.as_view()),
    url(r'^statistical/day_active/$', home_views.UserDayActiveView.as_view()),
    url(r'^statistical/day_increment/$', home_views.UserDayIncrementView.as_view()),
    url(r'^statistical/day_orders/$', home_views.UserDayOrdersView.as_view()),

    url(r'^statistical/month_increment/$', home_views.UserMonthIncrementView.as_view()),
    url(r'^statistical/goods_day_views/$', home_views.GoodCategoryDayView.as_view()),
]
