from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
from datetime import date, timedelta
from rest_framework.permissions import IsAdminUser


# 5, 获取月增用户
class UserMonthIncrementView(APIView):
    # 1, 设置管理员权限
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 1, 获取30天前的时间
        old_date = date.today() - timedelta(days=30)

        # 2, 拼接数据
        count_list = []
        for i in range(1, 31):
            # 2,1 获取当天时间
            current_date = old_date + timedelta(days=i)

            # 2,3 获取当天时间的下一天
            next_date = old_date + timedelta(days=i + 1)

            # 2,4, 查询用户日增数量, 注意点: date.today() 获取的不带时分秒
            count = User.objects.filter(date_joined__gte=current_date, date_joined__lt=next_date,
                                        is_staff=False).count()

            count_list.append({
                "count": count,  # 字典中的key 必须是字符串 count 必须加引号
                "date": current_date
            })

        # 2, 返回响应
        return Response(count_list)
