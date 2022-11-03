from rest_framework import serializers
from orders.models import OrderInfo, OrderGoods
from goods.models import SKU


class SKUSerializer(serializers.ModelSerializer):
    """
        sku商品序列化器
    """

    class Meta:
        model = SKU
        fields = ('name', 'default_image_url')


class OrderGoodsSerializer(serializers.ModelSerializer):
    """
        订单商品序列化器
    """
    # 副表用外键key值 sku
    sku = SKUSerializer()  # 具体一个一个的商品 都放在同一个订单中 此处不用 many=True

    class Meta:
        model = OrderGoods  # 外键关联 关键字
        fields = ('count', 'price', 'sku')


class OrederSerialzier(serializers.ModelSerializer):
    """
        订单序列化器
    """
    # 主表用外键关联的 related_name 字段值
    # 一个订单内，可以有多个商品，此处是一对多的关系
    skus = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = '__all__'
