from rest_framework import serializers
from django.db import transaction  # 事务对应的包
# from celery_tasks.static_file.tasks import get_detail_html
from goods.models import SKU, GoodsCategory, SPUSpecification, SpecificationOption, SKUSpecification


class SKUSpecificationSerializer(serializers.ModelSerializer):
    """
            sku具体规格表数据
    """
    spec_id = serializers.IntegerField()
    option_id = serializers.IntegerField()

    class Meta:
        model = SKUSpecification
        fields = ('spec_id', 'option_id')


class SKUSerialzier(serializers.ModelSerializer):
    """
        sku序列化器
    """

    # 注意外键关联字段需要前后端匹配
    spu_id = serializers.IntegerField()
    category_id = serializers.IntegerField()

    # specificationoption_set {}.spec_id
    specs = SKUSpecificationSerializer(read_only=True, many=True)

    class Meta:
        model = SKU
        fields = "__all__"
        read_only_fields = ('spu', 'category')  # 去掉序列化器中 不入库的字段

    # @transaction.atomic()  # 开启事务的方式一
    def create(self, validated_data):
        """
        保存sku新增信息时，有三张表联查结果，需要同时添加: 要么都成功，要么都失败[经典的事务操作]
        validated_data 内无spu_id, category_id这两个字段
        保存sku表数据 -> validated_data 内获取
        保存sku具体规格表 ->

        事务操作流程:
        1 引入包 from django.db import transaction
        2 开启事务（两种方式）
            a @transaction.atomic() 写在函数名的前面
            b with transaction.atomic():
        3 执行事务
            with transaction.atomic():
                # 设置保存点
                save_point = transaction.savepoint()
                try:
                    # 保存sku表
                    # 保存sku具体规格表
                expect:
                    # 回滚
                    transaction.savepoint_rollback(save_point)
                    raise serializers.ValidationError('保存失败')
                else:
                    # 提交
                    transaction.savepoint_commit(save_point)

                    return sku

        """
        specs = self.context['request'].data.get('specs')  # 牛逼的数据查找
        # 开启事务 方式二
        with transaction.atomic():
            # 设置保存点
            save_point = transaction.savepoint()
            try:
                # 保存sku表
                sku = SKU.objects.create(**validated_data)
                # 保存sku具体规格表
                for spec in specs:
                    SKUSpecification.objects.create(spec_id=spec['spec_id'], option_id=spec['option_id'], sku=sku)

            except:
                # 回滚
                transaction.savepoint_rollback(save_point)
                raise serializers.ValidationError('保存失败')

            else:
                # 提交
                transaction.savepoint_commit(save_point)

                # 生成详情页的静态页面
                # get_detail_html.delay(sku.id)

                return sku

    def update(self, instance, validated_data):
        specs = self.context['request'].data.get('specs')
        # 开启事务
        with transaction.atomic():
            # 设置保存点
            save_point = transaction.savepoint()
            try:
                # 修改sku表
                SKU.objects.filter(id=instance.id).update(**validated_data)
                # 修改sku具体规格表
                for spec in specs:
                    SKUSpecification.objects.filter(sku=instance).update(**spec)
                    # SKUSpecification.objects.filter(sku=instance,spec_id=spec['spec_id']).update(**spec)

            except:
                # 回滚
                transaction.savepoint_rollback(save_point)
                raise serializers.ValidationError('保存失败')

            else:
                # 提交
                transaction.savepoint_commit(save_point)

                # 生成详情页的静态页面
                # get_detail_html.delay(instance.id)

                return instance


class GoodsCategorySerializer(serializers.ModelSerializer):
    """
        商品分类序列化器
    """

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class SpecificationOptionSerializer(serializers.ModelSerializer):
    # SPU规格序选项列化器（副表）
    class Meta:
        model = SpecificationOption
        fields = '__all__'


class SPUSpecificationSerializer(serializers.ModelSerializer):
    """
        SPU规格序列化器(主表)
    """
    # 默认主表关联副表的字段使用，如果 有related_name = options ，就可以使用自定义字段 option
    # specificationoption_set=SpecificationOption(many=True)

    options = SpecificationOptionSerializer(many=True)  # many=True 一对多的关系

    class Meta:
        model = SPUSpecification
        fields = '__all__'
