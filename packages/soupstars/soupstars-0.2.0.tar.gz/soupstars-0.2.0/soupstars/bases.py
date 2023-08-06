import hashlib
import json
import os
import re

import bs4
import requests
from flask import request, jsonify


from .caches import DefaultCache, RedisCache


def parse(func):
    func.__parser__ = True
    return func


def load_best_cacher():
    if os.environ.get("SOUPSTARS_REDIS_URL"):
        return RedisCache
    else:
        return DefaultCache


class Parser(object):

    @classmethod
    def _return_args(klass, *args, lazy=False):
        return args


    @classmethod
    def endpoint(klass):
        """
        Convert a parser into a route based on its class name.

        >>> route_for_parser(NytimesArticleParser)
        /nytimes/article
        """

        parser_class_name = re.findall('[A-Z][^A-Z]*', klass.__name__)
        route_first_component, route_second_component = parser_class_name[:2]
        return "/{fc}/{sc}".format(
            fc=route_first_component.lower(),
            sc=route_second_component.lower()
        )

    @classmethod
    def view_function(klass):
        """
        Initialize the parser based on the args passed to the view func and
        return the jsonify(parser) value
        """

        parser = klass(**request.json)
        return jsonify(data=parser.dict())


    loader = _return_args
    reader = _return_args
    cacher = load_best_cacher()


    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        try:
            self._lazy = self._kwargs.pop('lazy')
        except KeyError:
            self._lazy = False
        self.cache_id = self._cache_id()
        self.cacher = self.__class__.cacher()
        self._set_parsers()
        if not self._lazy:
            self._load()


    def _cache_id(self):
        args_value = "_".join(self._args)

        kwargs_strings = [':'.join(str(item) for item in self._kwargs.items())]
        if kwargs_strings:
            kwargs_value = '_'.join(kwargs_strings)
        else:
            kwargs_value = ""

        name_value = self.__class__.__name__
        string_value = " | ".join([args_value, kwargs_value, name_value])
        hash_value = hashlib.md5(string_value.encode('utf8'))
        return hash_value.hexdigest()


    def _load(self):
        cached_load = self.cacher.get(self.cache_id)
        if cached_load:
            return cached_load
        else:
            load = self.__class__.loader(*self._args, **self._kwargs)
            self.cacher.set(self.cache_id, load)
            return load


    def _read(self):
        return self.__class__.reader(self._load())


    def _set_parsers(self):
        if hasattr(self, '_parsers'):
            return self._parsers
        else:
            self._parsers = {}
            for attr_name in dir(self):
                attr = getattr(self, attr_name)
                if hasattr(attr, "__parser__"):
                    self._parsers[attr_name] = attr
            else:
                return self._parsers


    def __getitem__(self, key):
        return self._parsers[key].__call__()


    def tuples(self):
        for parser_name, parser in self._parsers.items():
            yield parser_name, parser()

    def dict(self):
        return dict(self.tuples())


    def json(self):
        return json.dumps(self.dict())


    def read(self):
        return self._read()


    def load(self):
        return self._load()


class HttpParser(Parser):

    # Note that default host should not end in a /
    default_host = "http://0.0.0.0"
    default_route = "/"

    @classmethod
    def _loader(klass, **kwargs):
        """
        """

        try:
            url = kwargs.pop('url')
        except KeyError:
            url = klass.default_route
        if klass.default_host is not None:
            url = klass.default_host + url
        return requests.get(url, **kwargs).content


    loader = _loader
    reader = lambda x: bs4.BeautifulSoup(x, features="html.parser")
