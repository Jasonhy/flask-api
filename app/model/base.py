# -*- coding:utf-8 -*-

"""
@author: Jason
@desc: 模型基类
@time: 2018/10/21 8:16
"""
from datetime import datetime
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Integer, Column, SmallInteger

from app.libs.error_code import NotFound


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    """
    覆盖查询类,主要是为了重写filter_by方法
    """

    def filter_by(self, **kwargs):
        if "status" not in kwargs.keys():
            kwargs["status"] = 1
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident):
        rv = self.get(ident)
        if not rv:
            raise NotFound()
        else:
            return rv

    def first_or_404(self):
        rv = self.first()
        if not rv:
            raise NotFound()
        else:
            return rv


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True
    create_time = Column(Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != id:
                setattr(self, key, value)

    def delete(self):
        self.status = 0

    def keys(self):
        return self.fields

    def hide(self, *keys):
        """
        字段隐藏
        :param keys:
        :return:
        """
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        """
        添加字段
        :param keys:
        :return:
        """
        for key in keys:
            self.fields.append(key)
        return self
