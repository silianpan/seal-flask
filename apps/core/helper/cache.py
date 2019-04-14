#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-14 18:29
# @Author  : liupan
# @Site    : 
# @File    : cache.py
# @Software: PyCharm

import hashlib
import memcache
import traceback
from flask import request
from functools import wraps
from apps.app import app
from werkzeug.contrib.cache import MemcachedCache

mc = memcache.Client()
cache = MemcachedCache(mc)


def cached(fn=None, unique_per_user=True, minutes=30):
    """Caches a Flask route/view in memcached.

    The request url, args, and current user are used to build the cache key.
    Only GET requests are cached.
    By default, cached requests expire after 30 minutes.
    """

    if not isinstance(minutes, int):
        raise Exception('Minutes must be an integer number.')

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if request.method != 'GET':
                return func(*args, **kwargs)

            prefix = 'flask-request'
            path = request.full_path
            user_id = app.current_user.id if app.current_user.is_authenticated else None
            key = u('{user}-{method}-{path}').format(
                user=user_id,
                method=request.method,
                path=path,
            )
            hashed = hashlib.md5(key.encode('utf8')).hexdigest()
            hashed = '{prefix}-{hashed}'.format(prefix=prefix, hashed=hashed)

            try:
                resp = cache.get(hashed)
                if resp:
                    return resp
            except:
                app.logger.error(traceback.format_exc())
                resp = None

            resp = func(*args, **kwargs)
            try:
                cache.set(hashed, resp, timeout=minutes * 60)
            except:
                app.logger.error(traceback.format_exc())
            return resp

        return inner
    return wrapper(fn) if fn else wrapper
