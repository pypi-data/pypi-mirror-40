import redis
import pickle
import os


class BaseCache(object):

    def get(self, key):
        return self.cache.get(key)

    def set(self, key):
        return self.cache.set(key)


class DefaultCache(dict):
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value


class RedisCache(dict):
    def __init__(self, *args, **kwargs):
        try:
            self.URL = os.environ['SOUPSTARS_REDIS_URL']
        except KeyError:
            msg = """Couldn't find a redis url in the environment. You need to
            set SOUPSTARS_REDIS_URL in order to use a redis backend.
            """
            raise KeyError(msg)

        self._cache = redis.Redis.from_url(self.URL)

    def get(self, key):
        pickled_value = self._cache.get(key)
        if pickled_value is None:
            return None
        return pickle.loads(pickled_value)

    def set(self, key, value):
        pickled_value = pickle.dumps(value)
        self._cache.set(key, pickled_value, ex=60*60*24)  # 1 day
