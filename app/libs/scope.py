# -*- coding:utf-8 -*-

"""
@author: Jason
@desc: 定义访问域
@time: 2018/10/21 17:15
"""


class Scope:
    # 允许访问的视图函数
    allow_api = []
    # 添加模块,如果一个用户能够访问一个模块下所有的
    # 视图函数,就可以将这个模块添加进来
    allow_module = []

    # 排除一些不可以访问的视图函数
    forbidden = []

    def __add__(self, other):
        # 实现对象的加号运算
        # 运算符重载
        self.allow_api = self.allow_api + other.allow_api
        self.allow_api = list(set(self.allow_api))

        self.allow_module = self.allow_module + other.allow_module
        self.allow_module = list(set(self.allow_module))

        self.forbidden = self.forbidden + other.forbidden
        self.forbidden = list(set(self.forbidden))

        return self


class AdminScope(Scope):
    # allow_api = ["v1.user+super_get_user",
    #              "v1.user+super_delete_user"]
    allow_module = ["v1.user"]

    def __init__(self):
        # self + UserScope()
        # print(self.allow_api)
        pass


class UserScope(Scope):
    # allow_api = ["v1.user+get_user","v1.user+delete_user"]
    # 通过排除的方式来配置
    forbidden = ["v1.user+super_get_user",
                 "v1.user+super_delete_user"]

    def __init__(self):
        self + AdminScope()


class SuperScope(Scope):
    allow_api = ["v1.C", "v1.D"]
    allow_module = ["v1.user"]

    def __init__(self):
        self + UserScope() + AdminScope()
        # print(self.allow_api)


# SuperScope()
# AdminScope()


def is_in_scope(scope, endpoint):
    """
    判断能访问哪个视图函数
    :param scope: 根据scope找到对应的Scope
    :param endpoint: 对其进行修改 v.view_func  => v1.module_name+v1.view_func
                      => v1.red_name+v1.view_func
    :return:
    """
    gl = globals()
    # 通过globals获取对应的scope
    scope = gl[scope]()
    splits = endpoint.split("+")
    red_name = splits[0]
    if endpoint in scope.forbidden:
        return False
    if endpoint in scope.allow_api:
        return True
    if red_name in scope.allow_module:
        return True
    else:
        return False
