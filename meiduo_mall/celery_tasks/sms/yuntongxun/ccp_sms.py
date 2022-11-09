# -*- coding:utf-8 -*-
# https://www.yuntongxun.com/member/main 查看
# from .CCPRestSDK import REST 🙅‍
from celery_tasks.sms.yuntongxun.CCPRestSDK import REST  # 导入模版必须是 source Root目录

# 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
_accountSid = '8aaf0708842397dd0184563121740fdb'

# 说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
_accountToken = '68d72f48ed2743aeb614c422331afd1d'

# 请使用管理控制台首页的APPID或自己创建应用的APPID
_appId = '8aaf0708842397dd0184563dfabd0fe8'

# 说明：请求地址，生产环境配置成app.cloopen.com
_serverIP = 'sandboxapp.cloopen.com'

# 说明：请求端口 ，生产环境为8883
_serverPort = "8883"

# 说明：REST API版本号保持不变
_softVersion = '2013-12-26'

# 云通讯官方提供的发送短信代码实例
# # 发送模板短信
# # @param to 手机号码
# # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# # @param $tempId 模板Id
#
# def sendTemplateSMS(to, datas, tempId):
#     # 初始化REST SDK
#     rest = REST(serverIP, serverPort, softVersion)
#     rest.setAccount(accountSid, accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to, datas, tempId)
#     for k, v in result.iteritems():
#
#         if k == 'templateSMS':
#             for k, s in v.iteritems():
#                 print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)


class CCP(object):
    """发送短信的辅助类-单例类
    1 判断单例是否存在
    2 如果单例不存在，初始化单例
    3 返回单例

    将应用绑定到单例属性的子属性上，实现应用一定是单例(应用和单例 同生共死)
    """

    def __new__(cls, *args, **kwargs):
        # 判断是否存在类属性_instance，_instance是类CCP的唯一对象，即单例
        if not hasattr(CCP, "_instance"):
            # 如果单例不存在，初始化单例
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)

            # 初始化rest sdk -> 将应用绑定到单例属性的子属性上，实现应用一定是单例(应用和单例 同生共死)
            cls._instance.rest = REST(_serverIP, _serverPort, _softVersion)
            cls._instance.rest.setAccount(_accountSid, _accountToken)
            cls._instance.rest.setAppId(_appId)

        # 返回单例
        return cls._instance

    def send_template_sms(self, to, datas, temp_id):
        """发送模板短信"""
        # 发送短信验证码 - 调用时 - 单例方法

        # @param to 手机号码
        # @param datas 内容数据 格式为数组[短信验证码内容, 短信验证码时间间隔] 例如：{'12','34'}，如不需替换请填 ''
        # @param temp_id 模板Id
        # @return 成功 0 失败 -1
        result = self.rest.sendTemplateSMS(to, datas, temp_id)
        print(result)  # 发送短信码的时间延迟很明显，可优化
        # 如果云通讯发送短信成功，返回的字典数据result中statuCode字段的值为"000000"
        if result.get("statusCode") == "000000":
            # 返回0 表示发送短信成功
            return 0
        else:
            # 返回-1 表示发送失败
            return -1


if __name__ == '__main__':
    ccp = CCP()
    # 注意： 测试的短信模板编号为1
    # 查看文档配置参数 http://doc.yuntongxun.com/pe/5a533e0c3b8496dd00dce08c
    # 5分钟过期
    ccp.send_template_sms('18479783236', ['123456', 5], 1)