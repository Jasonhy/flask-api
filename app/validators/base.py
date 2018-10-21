# -*- coding:utf-8 -*-

"""
@author: Jason
@desc: 重构wtform
@time: 2018/10/21 11:43
"""
from flask import request
from wtforms import Form

from app.libs.error_code import ParameterException


class BaseForm(Form):

    def __init__(self):
        # data = request.json
        data = request.get_json(silent=True)  # 如果不是json数据,也不会报错
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data,**args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise ParameterException(msg=self.errors)

        return self
