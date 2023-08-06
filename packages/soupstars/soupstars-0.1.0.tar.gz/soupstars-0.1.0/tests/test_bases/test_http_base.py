from unittest.mock import patch, MagicMock

import pytest

mock_response = MagicMock()
mock_response.content = "<html><h1>Hello world</h1><p>From jim</p></html>"

def test_http_base_can_load():
    from soupstars import HttpBaseRecipe


@patch('requests.get')
def test_http_base_can_initialize(get):
    from soupstars import HttpBaseRecipe
    recipes = HttpBaseRecipe('myurl.com')
    assert get.called


@patch('requests.get', return_value=mock_response)
def test_http_recipe_can_parse(get, HttpRecipe):
    http_recipe = HttpRecipe('myurl.com')
    assert http_recipe['title'] == "Hello world"
    # print(requests.get)
