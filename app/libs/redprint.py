# -*- coding:utf-8 -*-

"""
@author: Jason
@desc: 通过redprint来构建模型路由
@time: 2018/10/20 15:17
"""


class Redprint:

    def __init__(self, name):
        """
        初始化
        :param name: 红图的名字
        """
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        """
        模仿蓝图的路由来设计红图路由
        :param rule:
        :param options:
        :return:
        """

        # 定义装饰器
        def decorator(f):
            self.mound.append((f, rule, options))

            return f

        return decorator

    def register(self, bp, url_prefix=None):
        """
        注册到蓝图
        :param bp: 蓝图
        :param url_prefix: url前缀
        :return:
        """
        if url_prefix is None:
            url_prefix = "/" + self.name

        for f, rule, options in self.mound:
            endpoint = self.name + "+" + options.pop("endpoint", f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)
