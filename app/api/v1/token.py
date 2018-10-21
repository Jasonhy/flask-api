# -*- coding:utf-8 -*-

"""
@author: Jason
@desc: 状态令牌
@time: 2018/10/21 13:33
"""
from flask import current_app, jsonify

from app.libs.enums import ClientTypeEnum
from app.libs.error_code import AuthFailed
from app.libs.redprint import Redprint
from app.model.user import User
from app.validators.forms import ClientForm, TokenForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

api = Redprint("token")


@api.route("", methods=["POST"])
def get_token():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify,
    }
    identity = promise[ClientTypeEnum(form.type.data)](
        form.account.data,
        form.secret.data
    )
    # Token
    expiration = current_app.config["TOKEN_EXPIRATION"]
    token = generate_auth_token(identity["uid"],
                                form.type.data,
                                identity["scope"],
                                expiration)

    t = {
        "token": token.decode("ascii")
    }
    return jsonify(t), 201


def generate_auth_token(uid, ac_type, scope=None, expiration=7200):
    """
    生成令牌
    :param uid:
    :param ac_type: 用户客户端类型
    :param scope: 权限作用域
    :param expiration: 过期时间
    :return:
    """
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
    return s.dumps({
        "uid": uid,
        "type": ac_type.value,
        "scope": scope
    })


@api.route('/secret', methods=['POST'])
def get_token_info():
    """获取令牌信息"""
    form = TokenForm().validate_for_api()
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(form.token.data, return_header=True)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)

    r = {
        'scope': data[0]['scope'],
        'create_at': data[1]['iat'],  # 令牌的创建时间
        'expire_in': data[1]['exp'],  # 令牌的有效期
        'uid': data[0]['uid']
    }
    return jsonify(r)
