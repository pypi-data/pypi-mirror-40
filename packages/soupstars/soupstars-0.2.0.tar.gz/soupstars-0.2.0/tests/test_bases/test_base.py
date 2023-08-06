from unittest.mock import patch

import pytest


def test_base_can_load():
    from soupstars import Parser, HttpParser


def test_base_can_initialize():
    from soupstars import Parser
    test_parser = Parser()


def test_load_can_run(test_parser):
    load = test_parser._load()


def test_lazy_load(TestParser):
    test_parser = TestParser(lazy=True)
    assert not test_parser.cacher.get(test_parser.cache_id)
    result = test_parser._load()
    assert result == test_parser.cacher.get(test_parser.cache_id)


def test_read_can_run(test_parser):
    test_parser._read()


@patch('soupstars.bases.Parser._load')
def test_read_triggers_load(_load, test_parser):
    test_parser._read()
    assert _load.called


def test_set_parsers_adds_functions(test_parser):
    assert 'spices' in test_parser._parsers
    assert 'not_spices' not in test_parser._parsers
    assert test_parser.spices == test_parser._parsers['spices']


def test_get_item_can_run(test_parser):
    assert test_parser['spices'] == test_parser.spices()


def test_get_item_can_run_with_lazy_loading(TestParser):
    test_parser = TestParser(lazy=True)
    assert test_parser["spices"] == test_parser.spices()


def test_subclass_uses_new_loader():
    from soupstars import Parser

    class SubParser(Parser):
        loader = lambda x: 'some_value'

    p = SubParser('a')
    assert p._load() == 'some_value'
