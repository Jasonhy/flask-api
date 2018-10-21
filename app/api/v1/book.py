# -*- coding:utf-8 -*-

"""
@author: Jason
@desc: 操作book
@time: 2018/10/20 15:10
"""

from flask import Blueprint, jsonify
from sqlalchemy import or_

from app.libs.redprint import Redprint

# book = Blueprint("book", __name__)  # 使用蓝图构建路由
from app.model.book import Book
from app.validators.forms import BookSearchForm

api = Redprint("book")  # 使用红图的方式


@api.route("/search")
def search():
    form = BookSearchForm()
    q = "%" + form.q.data + "%"
    # 模糊查询
    books = Book.query.filter(
        or_(Book.title.like(q), Book.publisher.like(q))
    ).all()

    # 支持模型的隐藏字段
    books = [book.hide("summary") for book in books]
    return jsonify(books)


@api.route("/<isbn>/detail")
def detail(isbn):
    book = Book.query.filter_by(isbn=isbn).first_or_404()
    return jsonify(book)
