# -*- coding:utf-8 -*-

"""
@author: Jason
@desc: 项目入口
@time: 2018/10/20 14:58
"""
from werkzeug.exceptions import HTTPException

from app import create_app
from app.libs.error import APIException
from app.libs.error_code import ServerError

app = create_app()


# 全局捕获未知异常
@app.errorhandler(Exception)
def framework_error(e):
    """
    Exception可能性:
    1) APIException
    2) HTTPException
    3) 原生的Exception
    :param e:
    :return:
    """
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg=msg, code=code, error_code=error_code)
    else:
        # 实际中会添加日志记录 log
        # 如果是调试模式,返回全部信息
        if not app.config["DEBUG"]:
            return ServerError()
        else:
            raise e


if __name__ == '__main__':
    app.run(debug=True)
