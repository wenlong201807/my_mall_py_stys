from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from meiduo_admin.serialziers.admin import AdminSerializer
from meiduo_admin.serialziers.group import GroupSerialzier
from meiduo_mall.utils.my_pagination import MyPageNumberPagination
from users.models import User
from django.contrib.auth.models import Group


class AdminView(ModelViewSet):
    # 父类方法需要调用序列化器
    serializer_class = AdminSerializer
    # c查询集属性
    queryset = User.objects.filter(is_staff=True)  # 普通管理员用户的特点是 is_staff=True
    # 分页属性
    pagination_class = MyPageNumberPagination
    # 权限属性
    permission_classes = [IsAdminUser]

    def simple(self, request):
        """
            获取分组信息
        :param request:
        :return:
        """
        # 1、查询分组表
        data = Group.objects.all()
        # 2、返回分组信息
        ser = GroupSerialzier(data, many=True)
        return Response(ser.data)
