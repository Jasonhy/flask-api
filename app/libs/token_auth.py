# -*- coding:utf-8 -*-

"""
@author: Jason
@desc: 用户认证
@time: 2018/10/21 14:09
"""
from collections import namedtuple

from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from app.libs.error_code import AuthFailed, Forbidden
from app.libs.scope import is_in_scope

auth = HTTPBasicAuth()
User = namedtuple("User", ["uid", "ac_type", "scope"])


@auth.verify_password
def verify_password(token, password):
    # 普通用户token:eyJhbGciOiJIUzUxMiIsImlhdCI6MTU0MDEyNjAyNywiZXhwIjoxNTQyNzE4MDI3fQ.eyJ1aWQiOjEsInR5cGUiOjEwMCwic2NvcGUiOiJVc2VyU2NvcGUifQ.Ig_Cg1KK-7hX7eFOpRfmlKqljLuIgIX0_9n9Y3cEcMasT3A55_hg46R2LUdGDh6DJPPb31mJQmuh523KjShz4Q
    # 超级管理员token:eyJhbGciOiJIUzUxMiIsImlhdCI6MTU0MDEyNTk0MSwiZXhwIjoxNTQyNzE3OTQxfQ.eyJ1aWQiOjE1LCJ0eXBlIjoxMDAsInNjb3BlIjoiQWRtaW5TY29wZSJ9.JELL413LYXTaJuf2KRcs2yxhZYKYR9vMPkONsWVbH6p2qDIS4-p3yAplVc6r_2-RkXdXhXT_5zVJSEVdZfmy4w
    # HTTP 自带账号密码 将账号和密码放到HTTP的header中
    # 传递规范:
    # key: Authorization
    # value: basic base64(jason:123456)
    # 直接将token放到Authorization中
    user_info = verify_auth_token(token=token)
    if not user_info:
        return False
    else:
        # 是用g属性,将user_info保存起来
        g.user = user_info
        return True


def verify_auth_token(token):
    s = Serializer(current_app.config["SECRET_KEY"])
    # 解密
    try:
        data = s.loads(token)
    except BadSignature:
        # 1) 验证合法性
        raise AuthFailed(
            msg="token is invalid",
            error_code=1002
        )
    except SignatureExpired:
        # 2) 验证有效期
        raise AuthFailed(
            msg="token is expired",
            error_code=1003
        )

    uid = data["uid"]
    ac_type = data["type"]
    scope = data["scope"]
    # request 可获取指定的视图函数
    allow = is_in_scope(scope,request.endpoint)
    if not allow:
        raise Forbidden()
    return User(uid, ac_type, scope)
