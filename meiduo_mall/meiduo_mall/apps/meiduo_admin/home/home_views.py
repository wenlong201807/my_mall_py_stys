from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from users.models import User
from datetime import date, timedelta
from rest_framework.permissions import IsAdminUser
from goods.models import CategoryVisitCount
from orders.models import OrderInfo
from . import home_serializers


# 1, 获取用户总数
class UserTotalCountView(APIView):
    # 1, 设置管理员权限
    permission_classes = [IsAdminUser]  # 局部添加接口访问权限

    def get(self, request):
        # 1, 查询用户总数 且过滤掉管理员用户 .filter(is_staff=False)
        count = User.objects.filter(is_staff=False).count()

        # 2, 返回响应
        return Response({
            "count": count
        })


# 2, 获取日活用户
class UserDayActiveView(APIView):
    # 1, 设置管理员权限
    permission_classes = [IsAdminUser]  # 局部添加接口访问权限

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
    permission_classes = [IsAdminUser]  # 局部添加接口访问权限

    def get(self, request):
        # 1, 查询用户日增数量, 注意点: date.today() 获取的不带时分秒
        count = User.objects.filter(date_joined__gte=date.today(), is_staff=False).count()

        # 2, 返回响应
        return Response({
            "count": count
        })


# 4, 获取日下单用户
class UserDayOrdersView(APIView):
    # 1, 设置管理员权限
    permission_classes = [IsAdminUser]  # 局部添加接口访问权限

    def get(self, request):
        # 1, 查询用户日下单用户数量
        count = User.objects.filter(orderinfo__create_time__gte=date.today(), is_staff=False).count()
        # count = User.objects.filter(haha__create_time__gte=date.today(), is_staff=False).count()
        # 方式二 [更合理] 此功能使用orderinfo表查询更恰当  requese 为当前用户数据 user_id=request.user.id
        cot = OrderInfo.objects.filter(create_time__gte=date.today()).count()

        # 2, 返回响应
        return Response({
            # "count": count
            "count": cot
        })


# 5, 获取月增用户
class UserMonthIncrementView(APIView):
    # 1, 设置管理员权限
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 1, 获取30天前的时间
        old_date = date.today() - timedelta(days=30)

        # 2, 拼接数据
        count_list = []
        for i in range(1, 31):
            # 2,1 获取当天时间
            current_date = old_date + timedelta(days=i)

            # 2,3 获取当天时间的下一天
            next_date = old_date + timedelta(days=i + 1)

            # 2,4, 查询用户日增数量, 注意点: date.today() 获取的不带时分秒
            count = User.objects.filter(date_joined__gte=current_date, date_joined__lt=next_date,
                                        is_staff=False).count()

            count_list.append({
                "count": count,  # 字典中的key 必须是字符串 count 必须加引号
                "date": current_date
            })

        # 2, 返回响应
        return Response(count_list)


# 6, 获取商品日分类访问量
class GoodCategoryDayView(ListAPIView):
    """
    ListAPIView:
    1, 父类是GenericAPIView + ListModelMixin ,
    2, 提供了get方法, 获取所有数据

    只要是能够用到序列化器的，就可以使用二级以上的视图

    serializer_class 将数据源转化成指定的序列化数据
    queryset 数据源，来源于数据表中的。

    业务需求规定： 过滤出今天查看的商品，其他日期的访问量不展示
    """
    serializer_class = home_serializers.CategoryVisitCountSerializer
    queryset = CategoryVisitCount.objects.filter(date=date.today()).all()
