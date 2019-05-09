#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-13 20:32
# @Author  : liupan
# @Site    : 
# @File    : dict_api.py
# @Software: PyCharm

from apps.core.db.mysql import db
from apps.core.model.base_model import BaseModel


class DictGroup(BaseModel):
    __tablename__ = 't_dict_group'

    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(1024))
    enable = db.Column(db.Boolean)

    _default_fields = ["id", "del_flag", "crt_time", "name", "code", "enable", "description"]

    def __repr__(self):
        return '<DictGroup %r>' % self.name
