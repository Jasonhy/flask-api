# -*- coding:utf-8 -*-

"""
@author: Jason
@desc: 
@time: 2018/10/21 10:50
"""
from datetime import date

from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder

from app.libs.error_code import ServerError


class JSONEncode(_JSONEncoder):

    def default(self, o):
        # 判断是否存在keys 和 __getitem__
        if hasattr(o, "keys") and hasattr(o, "__getitem__"):
            return dict(o)
        # 处理不能序列化的数据类型
        if isinstance(o, date):
            return o.strftime("%Y-%m-%d")
        raise ServerError()


class Flask(_Flask):
    # 使用我们自己定义的JSONEncode
    json_encoder = JSONEncode

