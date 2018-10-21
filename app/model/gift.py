# -*- coding:utf-8 -*-

"""
@author: Jason
@desc: 礼物模型
@time: 2018/10/21 23:45
"""
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from app.model.base import Base


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)



