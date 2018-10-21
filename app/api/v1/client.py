# -*- coding:utf-8 -*-

"""
@author: Jason
@desc: 客户端注册
@time: 2018/10/20 17:03
"""
from flask import request

from app.libs.enums import ClientTypeEnum
from app.libs.error_code import ClientTypeError, Success
from app.libs.redprint import Redprint
from app.model.user import User
from app.validators.forms import ClientForm, UserEmailForm

api = Redprint("client")


@api.route("/register", methods=["POST"])
def create_client():
    # 注册
    # 使用自己的验证器
    # 定义为以json的数据进行提交,可通过request.json和request.args.to_dict()的形式获取数据
    # data = request.json
    # 对数据进行验证
    form = ClientForm().validate_for_api()
    # form.validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email
    }

    promise[form.type.data]()
    return Success()


def __register_user_by_email():
    form = UserEmailForm().validate_for_api()
    # form.validate_for_api()
    User.register_by_email(form.nickname.data, form.account.data, form.secret.data)
