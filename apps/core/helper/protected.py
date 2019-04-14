#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-14 18:48
# @Author  : liupan
# @Site    : 
# @File    : protected.py
# @Software: PyCharm

import redis
import traceback
from flask import request
from functools import wraps
from apps.app import app
from werkzeug.exceptions import NotFound

r = redis.Redis(decode_responses=True)


def protected(fn=None, limit=10, minutes=60):
    """Bans IP after requesting a protected resource too many times.

    Prevents IP from making more than `limit` requests per `minutes` to
    the decorated route. Prevents enumerating secrets or tokens from urls or
    query arguments by blocking requests after too many 404 not found errors.
    """

    if not isinstance(limit, int):
        raise Exception('Limit must be an integer number.')
    if not isinstance(minutes, int):
        raise Exception('Minutes must be an integer number.')

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            key = u('bruteforce-{}-{}').format(request.endpoint, request.remote_addr)
            try:
                count = int(r.get(key) or 0)
                if count > limit:
                    r.incr(key)
                    seconds = 60 * minutes
                    r.expire(key, time=seconds)
                    app.logger.info('Request blocked by protected decorator.')
                    return '404', 404
            except:
                app.logger.error(traceback.format_exc())

            try:
                result = func(*args, **kwargs)
            except NotFound:
                try:
                    r.incr(key)
                    seconds = 60 * minutes
                    r.expire(key, time=seconds)
                except:
                    pass
                raise

            if isinstance(result, tuple) and len(result) > 1 and result[1] == 404:
                try:
                    r.incr(key)
                    seconds = 60 * minutes
                    r.expire(key, time=seconds)
                except:
                    pass

            return result

        return inner
    return wrapper(fn) if fn else wrapper
