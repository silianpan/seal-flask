#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-14 18:35
# @Author  : liupan
# @Site    : 
# @File    : rate_limited.py
# @Software: PyCharm

import redis
import traceback
from flask import abort, request
from functools import wraps
from apps.app import app

r = redis.Redis(decode_responses=True)


def rate_limited(fn=None, limit=20, methods=[], ip=True, user=True, minutes=1):
    """Limits requests to this endpoint to `limit` per `minutes`."""

    if not isinstance(limit, int):
        raise Exception('Limit must be an integer number.')
    if limit < 1:
        raise Exception('Limit must be greater than zero.')

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if not methods or request.method in methods:

                if ip:
                    increment_counter(type='ip', for_methods=methods,
                                      minutes=minutes)
                    count = get_count(type='ip', for_methods=methods)
                    if count > limit:
                        abort(429)

                    if user and app.current_user.is_authenticated:
                        increment_counter(type='user', for_methods=methods,
                                          minutes=minutes)
                        count = get_count(type='user', for_methods=methods)
                        if count > limit:
                            abort(429)

            return func(*args, **kwargs)

        return inner
    return wrapper(fn) if fn else wrapper


def get_counter_key(type=None, for_only_this_route=True, for_methods=None):
    if not isinstance(for_methods, list):
        for_methods = []
    if type == 'ip':
        key = request.remote_addr
    elif type == 'user':
        key = app.current_user.id if app.current_user.is_authenticated else None
    else:
        raise Exception('Unknown rate limit type: {0}'.format(type))
    route = ''
    if for_only_this_route:
        route = '{endpoint}'.format(
            endpoint=request.endpoint,
        )
    return u'{type}-{methods}-{key}{route}'.format(type=type, key=key, methods=','.join(for_methods), route=route)


def increment_counter(type=None, for_only_this_route=True, for_methods=None,
                      minutes=1):
    if type not in ['ip', 'user']:
        raise Exception('Type must be ip or user.')

    key = get_counter_key(type=type, for_only_this_route=for_only_this_route,
                          for_methods=for_methods)
    try:
        r.incr(key)
        r.expire(key, time=60 * minutes)
    except:
        app.logger.error(traceback.format_exc())
        pass


def get_count(type=None, for_only_this_route=True, for_methods=None):
    key = get_counter_key(type=type, for_only_this_route=for_only_this_route,
                          for_methods=for_methods)
    try:
        return int(r.get(key) or 0)
    except:
        app.logger.error(traceback.format_exc())
        return 0
