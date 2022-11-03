from django.conf import settings
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from goods.models import SKUImage, SKU
from meiduo_admin.serialziers.images import ImagesSerializer, SKUSerializer
from meiduo_mall.utils.my_pagination import MyPageNumberPagination
from rest_framework.permissions import IsAdminUser
# from fdfs_client.client import Fdfs_client


class ImagesView(ModelViewSet):
    queryset = SKUImage.objects.all()
    serializer_class = ImagesSerializer
    pagination_class = MyPageNumberPagination
    permission_classes = [IsAdminUser]

    def simple(self, request):
        """
            获取sku商品信息
        :param request:
        :return:
        """
        # 1、查询所有sku商品
        skus = SKU.objects.all()
        # 2、序列化返回
        ser = SKUSerializer(skus, many=True)  # 返回多条数据
        return Response(ser.data)

    # def create(self, request, *args, **kwargs):
    #     # 1、获取前端数据
    #     data = request.data
    #     # 2、验证数据
    #     ser = self.get_serializer(data=data)
    #     ser.is_valid()
    #     # # 3、建立fastdfs的客户端
    #     # client = Fdfs_client(settings.FASTDFS_PATH)
    #     # file = request.FILES.get('image')
    #     # # 4、上传图片
    #     # res = client.upload_by_buffer(file.read())
    #     # # 5、判断是否上传成功
    #     # if res['Status'] != 'Upload successed.':
    #     #     return Response({'error': '图片上传失败'})
    #     #
    #     # # 6、保存图片表
    #     # img = SKUImage.objects.create(sku=ser.validated_data['sku'], image=res['Remote file_id'])
    #
    #     ser.save()
    #     # 7、返回保存后的图片数据
    #     return Response(ser.data,status=201)
