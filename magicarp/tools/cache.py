"""
Cache
=====
"""

import zlib

from simple_settings import settings


class DummyEngine(object):
    def __init__(self):
        self.data = {}

    def setex(self, key, ttl, data):
        self.data[key] = data

    def get(self, key):
        return self.data[key]

    def delete(self, key):
        del self.data[key]

    def exists(self, key):
        return key in self.data

    def flushall(self):
        self.data = {}

    def flushdb(self):
        self.data = {}


def get_cache_engine():
    if not get_cache_engine.__dict__.get('engine'):
        if settings.CACHE_ENGINE == 'redis':
            import redis

            cache = redis.StrictRedis(
                host=settings.REDIS_HOST[0], port=settings.REDIS_HOST[1], db=0)

            if cache is None:  # pragma: no cover
                raise RuntimeError("Redis unavaibale")

            get_cache_engine.__dict__['engine'] = cache
        else:
            get_cache_engine.__dict__['engine'] = DummyEngine()

    return get_cache_engine.engine


def set_key(key, ttl, data, compress=True):
    '''Sets a key in the storage engine.

    It is done via redis Setex command. Compresses data via zlib.
    '''
    storage = get_cache_engine()

    if compress:
        data = zlib.compress(data)

    storage.setex(key, ttl, data)


def del_key(key):
    '''Deletes a key from storage'''
    storage = get_cache_engine()

    storage.delete(key)


def get_key(key, decompress=True):
    '''Gets a key and attempt to decompress it'''
    storage = get_cache_engine()

    data = storage.get(key)

    if data and decompress:
        try:
            data = zlib.decompress(data)
        except zlib.error:  # pragma: no cover
            pass

    return data


def key_exists(key):
    '''Checks if key exists'''
    storage = get_cache_engine()

    return storage.exists(key)


def flushdb():
    '''Checks if key exists'''
    storage = get_cache_engine()

    return storage.flushdb()


def flushall():
    '''Checks if key exists'''
    storage = get_cache_engine()

    return storage.flushall()
