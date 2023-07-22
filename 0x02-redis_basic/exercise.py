#!/usr/bin/env python3
""" Writing strings to Redis
"""

import uuid
import redis
from typing import Union, Callable
import functools


class Cache:
    def __init__(self):
        self._redis = redis.Redis()

    @functools.wraps
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store the input in Redis"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


def count_calls(method: Callable) -> Callable:
    """ Incrementing Value """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper
