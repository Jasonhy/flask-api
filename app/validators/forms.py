# -*- coding:utf-8 -*-

"""
@author: Jason
@desc: 验证
@time: 2018/10/20 17:10
"""
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError

from app.libs.enums import ClientTypeEnum
from app.validators.base import BaseForm as Form
from app.model.user import User


class ClientForm(Form):
    # 客户端验证
    # 不允许为空和添加长度限制
    account = StringField(validators=[DataRequired(message='不允许为空'), length(min=5, max=32)])  # 账号
    secret = StringField()  # 密码
    type = IntegerField(validators=[DataRequired()])  # 客户端类型

    # 希望type必须是我们定义的enum,所以需要自己定义验证器
    def validate_type(self, value):
        """
        自定义验证群
        :param value: 用户传过来的值
        :return:
        """

        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            # 如果不是枚举里的值,直接抛出异常
            raise e

        self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[Email(message="invalidate email")])  # 账号
    secret = StringField(validators=[
        DataRequired(),
        Regexp(r"^[A-Za-z0-9_*&$#@]{6,22}$")
    ])  # 密码
    nickname = StringField(
        validators=[DataRequired(), length(min=2, max=22)]
    )

    def validate_accout(self, value):
        """
        验证账号是否被使用过
        :return:
        """
        if User.query.filter_by(email=value.data).first():
            # 如果用户名存在,直接抛出异常
            raise ValidationError()


class BookSearchForm(Form):
    q = StringField(validators=[DataRequired()])


class TokenForm(Form):
    token = StringField(validators=[DataRequired()])
