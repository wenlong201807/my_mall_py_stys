from rest_framework.viewsets import ModelViewSet
from goods.models import SPU, Brand, GoodsCategory
from meiduo_admin.serialziers.spus import SPUGoodsSerialzier, SPUBrandsSerizliser, CategorysSerizliser
from meiduo_mall.utils.my_pagination import MyPageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action


class SPUGoodsView(ModelViewSet):
    """
        SPU表的增删改查
    """
    # 指定序列化器
    serializer_class = SPUGoodsSerialzier
    # 指定查询及
    queryset = SPU.objects.all()
    # 指定分页
    pagination_class = MyPageNumberPagination

    # 在类中跟定义获取品牌数据的方法
    def brand(self, request):
        # 1、查询所有品牌数据
        data = Brand.objects.all()
        # 2、序列化返回品牌数据
        ser = SPUBrandsSerizliser(data, many=True)

        return Response(ser.data)

    def channel(self, request):
        # 1、获取一级分类数据
        data = GoodsCategory.objects.filter(parent=None)
        # 2、序列化返回分类数据
        ser = CategorysSerizliser(data, many=True)
        return Response(ser.data)

    def channels(self, request, pk):
        # 1、获取二级和三级分类数据
        data = GoodsCategory.objects.filter(parent_id=pk)
        # 2、序列化返回分类数据
        ser = CategorysSerizliser(data, many=True)
        return Response(ser.data)