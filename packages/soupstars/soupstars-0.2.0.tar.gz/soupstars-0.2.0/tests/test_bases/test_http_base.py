from unittest.mock import patch, MagicMock

import pytest

mock_response = MagicMock()
mock_response.content = "<html><h1>Hello world</h1><p>From jim</p></html>"

def test_http_base_can_load():
    from soupstars import HttpParser


@patch('requests.get')
@patch('soupstars.caches.RedisCache.set')
def test_http_base_can_initialize(get, set):
    from soupstars import HttpParser
    recipes = HttpParser(url='myurl.com')
    assert get.called


@patch('requests.get', return_value=mock_response)
@patch('soupstars.caches.RedisCache.set')
def test_http_recipe_can_parse(get, set, TestHttpParser):
    http_recipe = TestHttpParser(url='myurl.com')
    assert http_recipe['title'] == "Hello world"
