#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 20:32
# @Author  : liupan
# @Site    : 
# @File    : dict_api.py
# @Software: PyCharm

from apps.core.db.mysql import db
from apps.core.model.base_model import BaseModel


class DictItem(BaseModel):
    __tablename__ = 't_dict_item'

    dict_value = db.Column(db.String(128), nullable=False)
    dict_key = db.Column(db.String(128), nullable=False)
    enable = db.Column(db.Boolean)
    group_code = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(128))
    config = db.Column(db.String(128))

    _default_fields = ["id", "del_flag", "crt_time", "dict_value", "dict_key", "enable", "group_code", "description"]

    def __repr__(self):
        return '<DictItem %r>' % self.dict_value
