from rest_framework import serializers
from goods.models import SKU, GoodsCategory, SPU, SPUSpecification, SpecificationOption


# 1, sku序列化器
class SKUSerializers(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = "__all__"


# 2, sku,category序列化器
class SKUCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ["id", "name"]


# 3, sku,spu序列化器
class GoodSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPU
        fields = ["id", "name"]


# 4, spec, option序列化器
class SpecOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationOption
        fields = ["id", "value"]


# sku,spu,specs序列化器
class GoodSpecsSerializer(serializers.ModelSerializer):
    # 1,规格关联的选项; 规格是一方, 选项是多方
    options = SpecOptionSerializer(read_only=True, many=True)

    class Meta:
        model = SPUSpecification
        fields = "__all__"
