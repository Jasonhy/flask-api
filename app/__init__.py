# -*- coding:utf-8 -*-

"""
@author: Jason
@desc: 实例化
@time: 2018/10/20 14:58
"""
from .app import Flask


def register_bluprints(app):
    """注册蓝图
    :param app: flask实例
    :return:
    """

    """
    不再使用多个蓝图的注册
    from app.api.v1.user import user
    from app.api.v1.book import book
    app.register_blueprint(user)
    app.register_blueprint(book)
    """

    # 使用公用的的蓝图
    from app.api.v1 import create_blueprint
    # 添加前缀
    app.register_blueprint(create_blueprint(), url_prefix="/v1")


def register_plugin(app):
    """
    注册用到的插件比如SQLAlchemy
    :param app:
    :return:
    """
    from app.model.base import db
    db.init_app(app)
    # create_all: 必须在上下文中生效
    with app.app_context():
        db.create_all()


def create_app():
    # 创建app
    app = Flask(__name__)
    # 加载配置文件
    app.config.from_object("app.config.setting")
    app.config.from_object("app.config.secure")

    # 注册
    register_bluprints(app)
    register_plugin(app)
    return app
