#!/usr/bin/env python3
""" Writing strings to Redis
"""

import redis
import uuid
from typing import Union, Callable
from functtools import wraps


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @wraps
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        """ store the input in Redis"""
        self._redis.set(key, data)

        return key


def count_calls(method: Callable) -> Callable:
    """ Incrementing Value """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)

        return method(self, *args, **kwargs)

    return wrapper
