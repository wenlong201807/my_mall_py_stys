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
        fields = ["id", "name"]  # 依据前端数据需求，只需要返回这两个字段内容即可


# 3, sku,spu序列化器
class GoodSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPU
        fields = ["id", "name"]


# 4, spec, option序列化器
class SpecOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationOption  # 三级关联 注意看model定义的外键关联 属性related_name
        fields = ["id", "value"]


# sku,spu,specs序列化器
class GoodSpecsSerializer(serializers.ModelSerializer):
    """
        联表查询功能 序列化器关联即可
        options = 此option 结果为外键关联中 属性related_name 的value

        关联的结果一般不只是获取id ，还需要其他字段，因此需要做扩展
    """
    # 1,规格关联的选项; 规格是一方, 选项是多方 -> 规格和选型 是 一对多的关系 -> many=True
    options = SpecOptionSerializer(read_only=True, many=True)
    # options = serializers.StringRelatedField(read_only=True, many=True)
    # options = serializers.PrimaryKeyRelatedField(read_only=True, many=True) 简单的关联查询

    class Meta:
        model = SPUSpecification
        fields = "__all__"
