from django.db import models


class BaseModel(models.Model):
    """
    作为基础类，每个模型都可以继承，算是统一封装吧
    此基类不会直接进入数据表中 <- abstract = True
    """
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        # 作用: 只能被继承使用, 不能被迁移
        abstract = True
