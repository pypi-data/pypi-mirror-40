from unittest.mock import patch

import pytest


def test_base_can_load():
    from soupstars import BaseRecipe, HttpBaseRecipe


def test_base_can_initialize():
    from soupstars import BaseRecipe
    recipes = BaseRecipe()


def test_load_can_run(recipe):
    load = recipe._load()


def test_lazy_load(Recipe):
    recipe = Recipe(lazy=True)
    assert not hasattr(recipe, "_cached_load")
    recipe._load()
    assert hasattr(recipe, "_cached_load")
    assert recipe._load() == recipe._cached_load


def test_read_can_run(recipe):
    recipe._read()


@patch('soupstars.bases.BaseRecipe._load')
def test_read_triggers_load(_load, recipe):
    recipe._read()
    assert _load.called


def test_set_ingredients_adds_functions(recipe):
    assert 'spices' in recipe._ingredients
    assert 'not_spices' not in recipe._ingredients
    assert recipe.spices == recipe._ingredients['spices']


def test_serialize_items_can_run(recipe):
    result = dict(recipe._serialize_items())
    assert result['spices'] == recipe.spices()
    assert "not_spices" not in result


def test_get_item_can_run(recipe):
    assert recipe['spices'] == recipe.spices()


def test_get_item_can_run_with_lazy_loading(Recipe):
    recipe = Recipe(lazy=True)
    assert not hasattr(recipe, "_cached_load")
    spices = recipe["spices"]
    assert spices == recipe.spices()
    assert hasattr(recipe, "_cached_load")
