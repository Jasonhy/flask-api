# -*- coding:utf-8 -*-

"""
@author: Jason
@desc: 礼物API
@time: 2018/10/21 23:47
"""
from flask import g

from app.libs.error_code import Success, DuplicateGift
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.model.base import db
from app.model.book import Book
from app.model.gift import Gift

api = Redprint("gift")


@api.route('/<isbn>', methods=['POST'])
@auth.login_required
def create(isbn):
    uid = g.user.uid
    with db.auto_commit():
        Book.query.filter_by(isbn=isbn).first_or_404()
        gift = Gift.query.filter_by(isbn=isbn, uid=uid).first()
        if gift:
            raise DuplicateGift()
        gift = Gift()
        gift.isbn = isbn
        gift.uid = uid
        db.session.add(gift)
    return Success()
