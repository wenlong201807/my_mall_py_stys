from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from goods.models import SpecificationOption, SPUSpecification
from meiduo_admin.serialziers.options import OptionSerialzier, OptionSpecificationSerializer
from meiduo_mall.utils.my_pagination import MyPageNumberPagination


class OptionsView(ModelViewSet):
    """
        规格选项表的增删改查
    """

    serializer_class = OptionSerialzier
    queryset = SpecificationOption.objects.all()
    pagination_class = MyPageNumberPagination


class OptionSimple(ListAPIView):
    """
        获取规格信息
    """
    serializer_class = OptionSpecificationSerializer
    queryset = SPUSpecification.objects.all()
