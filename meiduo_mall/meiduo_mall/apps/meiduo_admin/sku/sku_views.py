from rest_framework.viewsets import ModelViewSet
from meiduo_mall.utils.my_pagination import MyPageNumberPagination
from . import sku_serializers
from goods.models import SKU, GoodsCategory, SPU, SPUSpecification
from rest_framework.generics import ListAPIView


# 1, sku管理
class SKUModelViewSet(ModelViewSet):
    pagination_class = MyPageNumberPagination
    serializer_class = sku_serializers.SKUSerializers

    # queryset = SKU.objects.all()

    # 1,重写get_queryset,根据keyword过滤sku
    def get_queryset(self):

        # 1,获取keyword
        keyword = self.request.query_params.get("keyword")

        # 2,根据keyword查询sku
        if keyword:
            return SKU.objects.filter(name__contains=keyword).all()
        else:
            return SKU.objects.all()


# 2, sku,category
class SKUCategoryView(ListAPIView):
    pagination_class = None
    serializer_class = sku_serializers.SKUCategorySerializer
    #  如何约定是三级视图呢？根据约定的数据库内容约定： subs=None 或者  属于目标数据源
    queryset = GoodsCategory.objects.filter(subs=None).all()


# 3, sku,spu
class GoodSimpleView(ListAPIView):
    pagination_class = None
    serializer_class = sku_serializers.GoodSimpleSerializer
    queryset = SPU.objects.all()


# , sku, spu, specs
class GoodSpecsView(ListAPIView):
    """
    /meiduo_admin/goods/1/specs/
    接口路由中的参数? 如何获取 -> 两个需要一致 spu_id
    self.kwargs.get("spu_id") <-> url(r'^goods/(?P<spu_id>\d+)/specs/$',
    """
    pagination_class = None
    serializer_class = sku_serializers.GoodSpecsSerializer

    # queryset = SPUSpecification.objects.all()

    # 1,重写get_queryset,获取spu_id参数
    def get_queryset(self):
        # 1,如果要获取url中通过正则匹配到的参数,使用self.kwargs
        # print(self.kwargs)
        spu_id = self.kwargs.get("spu_id")

        # 2,返回数据源
        return SPUSpecification.objects.filter(spu_id=spu_id).all()
