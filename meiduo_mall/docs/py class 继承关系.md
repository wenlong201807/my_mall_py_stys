"""
view 的继承关系 查看源码 generics.py -> from rest_framework import generics
GenericViewSet(viewSet)   -drf
    GenericAPIView        -drf    
        APIView           -drf  过滤功能，序列化，分页
            View          -django
            
mixin  查看源码 mixins.py -> from rest_framework import mixins
   CreateModelMixin
   ListModelMixin  分页功能
   UpdateModelMixin 部分更新还是全部更新
   RetrieveModelMixin
   DestroyModelMixin 删除操作，并返回指定的状态码
"""