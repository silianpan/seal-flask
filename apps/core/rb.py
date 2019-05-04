#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-05-04 11:43
# @Author  : liupan
# @Site    : 
# @File    : rb.py
# @Software: PyCharm

from flask import jsonify


class Rb:
    """api调用返回结果"""

    @staticmethod
    def ok(data, code=0):
        """正确的返回结果"""
        return jsonify({'data': data, 'status': 0, 'code': code, 'msg': '成功'})

    @staticmethod
    def failed(msg='失败', code=-1):
        """失败的返回结果"""
        return jsonify({'data': None, 'status': -1, 'code': code, 'msg': msg})
