from magicarp import exceptions


class Engine(object):
    def __init__(self, **kwargs):
        try:
            import redis
        except ImportError:
            raise exceptions.MagicarpApiException(
                "Storage engine redis, could not import redis module "
                "(missing requirement?)")

        self._storage = redis.StrictRedis(**kwargs)

        if self._storage is None:
            raise exceptions.MagicarpApiException(
                "Could not connect to breathing redis instance")

    def set_key(self, key, value, **extra):
        self._storage.setex(key, extra['ttl'], value)

    def delete_key(self, key):
        self._storage.delete(key)

    def flush_all(self):
        self._storage.flushdb()

    def get_key(self, key):
        return self._storage.get(key)

    def key_exists(self, key):
        return self._storage.exists(key)
