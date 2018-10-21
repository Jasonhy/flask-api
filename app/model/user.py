# -*- coding:utf-8 -*-

"""
@author: Jason
@desc: 定义User模型
@time: 2018/10/20 22:52
"""
from sqlalchemy import Column, Integer, String, SmallInteger
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import NotFound, AuthFailed
from app.model.base import Base, db


class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True, nullable=False)
    nickname = Column(String(24), unique=True)
    # 主要是区分管理员和普通用户
    auth = Column(SmallInteger, default=1)
    _password = Column("password", String(100))

    # 提供自定义序列化使用
    def keys(self):
        return ["id", "email", "nickname", "auth"]

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        # 对密码进行加密
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_email(nickname, account, secret):
        """
        邮箱注册
        :param nickname:
        :param account:
        :param secret:
        :return:
        """
        user = User()
        user.nickname = nickname
        user.email = account
        user.password = secret
        with db.auto_commit():
            db.session.add(user)

    @staticmethod
    def verify(email, password):
        # user = User.query.filter_by(email=email).first()
        # if not user:
        #     raise NotFound(msg="user not found")
        user = User.query.filter_by(email=email).first_or_404()
        if not user.check_password(password):
            raise AuthFailed()
        # 添加是否是管理员信息
        scope = "AdminScope" if user.auth == 2 else "UserScope"
        return {"uid": user.id, "scope": scope}

    def check_password(self, raw):
        """
        密码校验
        :param raw:
        :return:
        """
        if not self._password:
            return False
        return check_password_hash(self._password, raw)
