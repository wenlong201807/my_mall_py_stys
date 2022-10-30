from django.db import models
from meiduo_mall.utils.my_model import BaseModel


class GoodsCategory(BaseModel):
    """商品类别"""
    name = models.CharField(max_length=10, verbose_name='名称')
    parent = models.ForeignKey('self', related_name='subs', null=True, blank=True, on_delete=models.CASCADE,
                               verbose_name='父类别')

    class Meta:
        db_table = 'tb_goods_category'
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CategoryVisitCount(models.Model):
    category = models.ForeignKey(GoodsCategory, verbose_name="商品分类", null=True, on_delete=models.CASCADE)
    count = models.IntegerField(default=0, verbose_name="访问量")
    date = models.DateField(verbose_name="访问日期")  # 写入的是年月日

    class Meta:
        db_table = "tb_category_visit_count"
