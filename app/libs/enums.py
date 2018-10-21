# -*- coding:utf-8 -*-

"""
@author: Jason
@desc: 定义枚举型数据
@time: 2018/10/20 17:06
"""
from enum import Enum


class ClientTypeEnum(Enum):
    # 客户端登录类型
    USER_EMAIL = 100
    USER_MOBILE = 101

    # 微信小程序
    USER_MINA = 200
    # 微信公众号
    USER_WX = 201



