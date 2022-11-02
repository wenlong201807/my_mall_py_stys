from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from goods.models import SPUSpecification
from goods.models import SPU
from meiduo_admin.serialziers.specs import SpecsSerialzier, SPUSerializer
# from meiduo_admin.utils import PageNum
from meiduo_mall.utils.my_pagination import MyPageNumberPagination


class SpecsView(ModelViewSet):
    """
        商品规格的增删改查
        继承的ModelViewSet 里头有增删改功能，是物理删除
    """
    # 指定查询集
    queryset = SPUSpecification.objects.all()
    # 指定序列化器
    serializer_class = SpecsSerialzier

    pagination_class = MyPageNumberPagination

    def simple(self, request):
        """
            获取SPU商品
        :param request:
        :return:
        """
        spus = SPU.objects.all()
        ser = SPUSerializer(spus, many=True)

        return Response(ser.data)

    # 如果约定为逻辑删除，则重写 父级的 destroy
    # def destroy(self, request, *args, **kwargs):
    #     spec = self.get_object()
    #     spec.is_delete = True
    #     spec.save()


