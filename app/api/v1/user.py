# -*- coding:utf-8 -*-

"""
@author: Jason
@desc: 操作user
@time: 2018/10/20 15:10
"""

from flask import Blueprint, jsonify, g

from app.libs.error_code import NotFound, DeleteSuccess
from app.libs.redprint import Redprint
from app.libs.token_auth import auth

# user = Blueprint("user", __name__)  # 使用蓝图构建路由
from app.model.base import db
from app.model.user import User

api = Redprint("user")  # 使用红图的方式


@api.route("/<int:uid>", methods=["GET"])
@auth.login_required
def super_get_user(uid):
    """
    超级管理员获取用户信息
    :param uid:
    :return:
    """
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


@api.route("/<int:uid>", methods=["DELETE"])
def super_delete_user(uid):
    """
    只有超级管理员用户才能去删除其他用户
    :param uid:
    :return:
    """
    pass


@api.route("", methods=["GET"])
@auth.login_required
def get_user():
    uid = g.user.uid
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


@api.route("", methods=["DELETE"])
@auth.login_required
def delete_user():
    # 账户注销
    # 应该是从token中获取uid,我们已经将用户数据存储在g变量中
    # g变量是线程隔离的,多个用户访问不会冲突
    uid = g.user.uid
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()


