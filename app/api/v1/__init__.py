# -*- coding:utf-8 -*-

"""
@author: Jason
@desc: 创建顶级蓝图,也就是公共蓝图
@time: 2018/10/20 15:10
"""
from flask import Blueprint
from app.api.v1 import user, book, client, token, gift


def create_blueprint():
    bp_v1 = Blueprint("v1", __name__)

    # 红图向蓝图的注册
    user.api.register(bp_v1)
    book.api.register(bp_v1)
    client.api.register(bp_v1)
    token.api.register(bp_v1)
    gift.api.register(bp_v1)

    return bp_v1
