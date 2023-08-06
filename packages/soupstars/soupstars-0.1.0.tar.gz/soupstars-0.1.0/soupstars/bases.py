import requests
import bs4
import json


def ingredient(func):
    func.__ingredient__ = True
    return func


class BaseRecipe(object):

    @classmethod
    def _return_args(klass, *args, lazy=False):
        return args


    loader = _return_args
    reader = _return_args
    serializer = lambda x: x


    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._lazy = kwargs.get('lazy') == True
        self._set_ingredients()
        if not self._lazy:
            self._load()


    def _load(self):
        if hasattr(self, '_cached_load'):
            return self._cached_load
        else:
            self._cached_load = self.__class__.loader(*self._args, **self._kwargs)
            return self._cached_load


    def _read(self):
        return self.__class__.reader(self._load())


    def _set_ingredients(self):
        if hasattr(self, '_ingredients'):
            return self._ingredients
        else:
            self._ingredients = {}
            for attr_name in dir(self):
                attr = getattr(self, attr_name)
                if hasattr(attr, "__ingredient__"):
                    self._ingredients[attr_name] = attr
            else:
                return self._ingredients


    def _serialize_items(self):
        for key in self._ingredients:
            yield key, self.__class__.serializer(self[key])


    def __getitem__(self, key):
        if not hasattr(self, '_cached_load'):
            self._load()
        return self._ingredients[key].__call__()


    def read(self):
        return self._read()


    def load(self):
        return self._load()


class HttpBaseRecipe(BaseRecipe):
    loader = lambda url: requests.get(url).content
    reader = lambda x: bs4.BeautifulSoup(x, features="html.parser")
    serializer = json.dumps

    def json(self):
        return json.dumps(dict(self._serialize_items()), indent=2)
