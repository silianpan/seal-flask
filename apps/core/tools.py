#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-14 23:15
# @Author  : liupan
# @Site    : 
# @File    : tools.py
# @Software: PyCharm

from flask import json
import re


class CustomEncoder(json.JSONEncoder):
    """A C{json.JSONEncoder} subclass to encode documents that have fields of
        type C{bson.objectid.ObjectId}, C{datetime.datetime}
    """
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


def to_tree(data=[]):
    for item in data:
        if 'children' in item.keys():
            del item['children']

    map = {}
    for item in data:
        map[item['id']] = item
    val = []
    for item in data:
        if item['pid'] in map.keys():
            parent = map[item['pid']]
            if 'children' not in parent.keys():
                parent['children'] = []
            parent['children'].append(item)
        else:
            val.append(item)
    return val


def hump2underline(hunp_str):
    '''
    驼峰形式字符串转成下划线形式
    :param hunp_str: 驼峰形式字符串
    :return: 字母全小写的下划线形式字符串
    '''
    # 匹配正则，匹配小写字母和大写字母的分界位置
    p = re.compile(r'([a-z]|\d)([A-Z])')
    # 这里第二个参数使用了正则分组的后向引用
    sub = re.sub(p, r'\1_\2', hunp_str).lower()
    return sub


def underline2hump(underline_str):
    '''
    下划线形式字符串转成驼峰形式
    :param underline_str: 下划线形式字符串
    :return: 驼峰形式字符串
    '''
    # 这里re.sub()函数第二个替换参数用到了一个匿名回调函数，回调函数的参数x为一个匹配对象，返回值为一个处理后的字符串
    sub = re.sub(r'(_\w)',lambda x:x.group(1)[1].upper(),underline_str)
    return sub
