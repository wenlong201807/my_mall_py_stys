from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date
from users.models import User
from rest_framework.permissions import IsAdminUser


# 1, 获取用户总数
class UserTotalCountView(APIView):
    # 1, 设置管理员权限
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 1, 查询用户总数 且过滤掉管理员用户 .filter(is_staff=False)
        count = User.objects.filter(is_staff=False).count()

        # 2, 返回响应
        return Response({
            "count": count
        })


# 2, 获取日活用户
class UserDayActiveView(APIView):
    def get(self, request):
        # 1, 查询用户日活数量
        count = User.objects.filter(last_login__gte=date.today(), is_staff=False).count()

        # 2, 返回响应
        return Response({
            "count": count
        })


# 3, 获取日增用户
class UserDayIncrementView(APIView):
    # 1, 设置管理员权限
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 1, 查询用户日增数量, 注意点: date.today() 获取的不带时分秒
        count = User.objects.filter(date_joined__gte=date.today(), is_staff=False).count()

        # 2, 返回响应
        return Response({
            "count": count
        })


# 4, 获取日下单用户
class UserDayOrdersView(APIView):
    def get(self, request):
        # 1, 查询用户日下单用户数量
        count = User.objects.filter(orderinfo__create_time__gte=date.today(), is_staff=False).count()

        # 2, 返回响应
        return Response({
            "count": count
        })
