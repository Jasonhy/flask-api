# -*- coding:utf-8 -*-

"""
@author: Jason
@desc: 创建管理员账户
@time: 2018/10/21 16:42
"""
from app import create_app
from app.model.base import db
from app.model.user import User

app = create_app()

with app.app_context():
    with db.auto_commit():
        user = User()
        user.nickname = "Super"
        user.password = "123456"
        user.email = "999@qq.com"
        user.auth = 2
        db.session.add(user)

