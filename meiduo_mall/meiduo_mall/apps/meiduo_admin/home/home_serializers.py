from rest_framework import serializers
from goods.models import CategoryVisitCount


# 1, 分类访问量序列化器
class CategoryVisitCountSerializer(serializers.ModelSerializer):
    """
        # 只要有参考的模型类来生成序列化器的字段，就考虑使用ModelSerializer

        数据表 tb_category_visit_count 中，外健关联的category_id 是数字，可是在前端页面需要展示其对应的中文，如何实现？

        # 方法1,重写category, 目的,在序列化的时候,将category数据,显示成汉字形式
        # category = serializers.StringRelatedField(read_only=True)

        本质上的流程是：
        1 查询此对应的model表设计的外健关联源 CategoryVisitCount
        2 关键关联源： category = models.ForeignKey(GoodsCategory, ...
        3 GoodsCategory 查询外健关联的表设计的 model 魔法函数 __str__ 的返回值
          将class GoodsCategory(BaseModel)中
              def __str__(self):
                  return self.name [最后会调用这个返回值展示中文]
    """
    # 方法2
    category = serializers.CharField(read_only=True)  # 多方关联一方 使用 read_only=True

    class Meta:
        model = CategoryVisitCount
        fields = "__all__"
