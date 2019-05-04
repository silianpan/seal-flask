#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-05-04 11:42
# @Author  : liupan
# @Site    : 
# @File    : util.py
# @Software: PyCharm

import bcrypt
import re


def get_hashed_password(plain_text_password, encoded_password):
    return bcrypt.hashpw(plain_text_password, encoded_password)


def check_password(plain_text_password, encoded_password):
    return bcrypt.checkpw(plain_text_password, get_hashed_password(plain_text_password, encoded_password))


def match_password(plain_text_password, encoded_password):
    """匹配登陆密码"""
    if re.match(r'\A\$2a?\$\d\d\$[./0-9A-Za-z]{53}', encoded_password):
        return check_password(plain_text_password, encoded_password)
    return False

