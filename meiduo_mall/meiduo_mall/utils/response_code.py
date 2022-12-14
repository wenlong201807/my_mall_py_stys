# coding:utf-8

class RET:
    OK                  = "0"
    DBERR               = "5000"
    IMAGECODEERR        = "4001"
    THROTTLINGERR       = "4002"
    NODATA              = "4002"
    DATAEXIST           = "4003"
    DATAERR             = "4004"
    SESSIONERR          = "4101"  # 判断用户是否是登录态
    LOGINERR            = "4102"
    PARAMERR            = "4103"
    USERERR             = "4104"
    ROLEERR             = "4105"
    PWDERR              = "4106"
    CPWDERR             = "4107"
    MOBILEERR           = "4108"
    REQERR              = "4201"
    IPERR               = "4202"
    THIRDERR            = "4301"
    IOERR               = "4302"
    SERVERERR           = "4500"
    UNKOWNERR           = "4501"
    NECESSARYPARAMERR   = "4502"
    SMSCODERR           = "4503"
    ALLOWERR            = "4504"


error_map = {
    RET.OK                    : u"成功",
    RET.DBERR                 : u"数据库查询错误",
    RET.NODATA                : u"无数据",
    RET.DATAEXIST             : u"数据已存在",
    RET.DATAERR               : u"数据错误",
    RET.SESSIONERR            : u"用户未登录",
    RET.LOGINERR              : u"用户登录失败",
    RET.PARAMERR              : u"参数错误",
    RET.USERERR               : u"用户不存在或未激活",
    RET.ROLEERR               : u"用户身份错误",
    RET.PWDERR                : u"密码错误",
    RET.CPWDERR               : u"密码不一致",
    RET.MOBILEERR             : u"手机号错误",
    RET.REQERR                : u"非法请求或请求次数受限",
    RET.IPERR                 : u"IP受限",
    RET.THIRDERR              : u"第三方系统错误",
    RET.IOERR                 : u"文件读写错误",
    RET.SERVERERR             : u"内部错误",
    RET.UNKOWNERR             : u"未知错误",
    RET.NECESSARYPARAMERR     : u"缺少必传参数",
    RET.SMSCODERR             : u"短信验证码有误",
    RET.ALLOWERR              : u"未勾选协议",
}
