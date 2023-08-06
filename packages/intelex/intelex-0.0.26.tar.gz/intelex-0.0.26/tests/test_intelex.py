from intelex import get_version, get_endpoint, get_apikey, _select_format, _count_format, _paginate_top_format, _paginate_skip_format, _generate_query_string
import os

def test_get_version():
    assert get_version() == '0.0.26'

def test_get_endpoint():
    assert get_endpoint() == os.environ['ilx_endpoint']

def test_get_aoikey():
    assert get_apikey() == os.environ['ilx_apikey']

def test_select_format():
    select_list = ['Hello', 'World', 'List']
    assert _select_format(select_list) == 'Hello, World, List'

def test_count_format_true():
    assert _count_format(True) == '$count=true'

def test_count_format_false():
    assert _count_format(False) == '$count=false'

def test_count_format_blank():
    assert _count_format() == '$count=false'

def test_paginate_top_format():
    assert _paginate_top_format(50) == '$top=50'

def test_paginate_skip_format():
    assert _paginate_skip_format(100) == '$skip=100'

def test_generate_query_string_all():
    query_string = {
        'select': ['RecordNumber', 'Id'],
        'count': True,
        'paginate_top': 50,
        'paginate_skip': 100
    }
    assert _generate_query_string(query_string) == '$select=RecordNumber, Id&$count=true&$top=50&$skip=100'


def test_generate_query_string_select():
    query_string = {
        'select': ['RecordNumber', 'Id']
    }
    assert _generate_query_string(query_string) == '$select=RecordNumber, Id'


def test_generate_query_string_count():
    query_string = {
        'count': True
    }
    assert _generate_query_string(query_string) == '$count=true'


def test_generate_query_string_top():
    query_string = {
        'paginate_top': 50
    }
    assert _generate_query_string(query_string) == '$top=50'


def test_generate_query_string_skup():
    query_string = {
        'paginate_skip': 100
    }
    assert _generate_query_string(query_string) == '$skip=100'
    
