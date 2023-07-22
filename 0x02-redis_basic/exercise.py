#!/usr/bin/env python3
""" Writing strings to Redis
"""

import redis
import uuid
from typing import Union, Callable
from functiontools import wraps

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

    def get(self, key: str, fn: callable = None) -> Union[str, bytes, int, float, None]:
        """retrievs data from Redis
        """
        data = self._redis.get(key)

        if data is None:
            return None

        if fn is not None:
            data = fn(data)

        return data

    def get_str(self, key: str) -> Union[str, None]:
        """paramize cache.get to string
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """parametrize cache.get int
        """
        return self.get(key, fn=int)

def count_calls(method: Callable) -> Callable:
    """ Incrementing Value """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)

        return method(self, *args, **kwargs)

    return wrapper
