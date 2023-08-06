import requests as r
import os
import json


# Private Functions

def _select_format(select_list):
    output = ', '
    output = output.join(select_list)
    return '{}'.format(output)


# Public Functions

def get_version():
    return '0.0.25'


def get_endpoint():
    ilx_endpoint = os.environ['ilx_endpoint']
    return ilx_endpoint


def get_apikey():
    ilx_apikey = os.environ['ilx_apikey']
    return ilx_apikey


def get_records(object, select=None):
    ilx_endpoint = os.environ['ilx_endpoint']
    ilx_apikey = os.environ['ilx_apikey']
    auth_header = 'Basic {}'.format(ilx_apikey)

    headers = {
        'Authorization': auth_header
    }

    if select != None:
        query = '{}/api/v2/object/{}?$select={}'.format(ilx_endpoint, object, _select_format(select))
    else:
        query = '{}/api/v2/object/{}'.format(ilx_endpoint, object)
    
    response = r.get(query, headers=headers)
    
    return json.loads(response.text)


def get_record(object, id):
    ilx_endpoint = os.environ['ilx_endpoint']
    ilx_apikey = os.environ['ilx_apikey']
    auth_header = 'Basic {}'.format(ilx_apikey)

    headers = {
        'Authorization': auth_header
    }

    query = '{}/api/v2/object/{}({})'.format(ilx_endpoint, object, id)

    response = r.get(query, headers=headers)

    return json.loads(response.text)


def get_related_records(object, id, navigation_property):
    ilx_endpoint = os.environ['ilx_endpoint']
    ilx_apikey = os.environ['ilx_apikey']
    auth_header = 'Basic {}'.format(ilx_apikey)

    headers = {
        'Authorization': auth_header
    }

    query = '{}/api/v2/object/{}({})/{}'.format(ilx_endpoint, object, id, navigation_property)
    response = r.get(query, headers=headers)

    return json.loads(response.text)


def get_related_record(object, id, navigation_property, related_id):
    ilx_endpoint = os.environ['ilx_endpoint']
    ilx_apikey = os.environ['ilx_apikey']
    auth_header = 'Basic {}'.format(ilx_apikey)

    headers = {
        'Authorization': auth_header
    }

    query = '{}/api/v2/object/{}({})/{}({})'.format(ilx_endpoint, object, id, navigation_property, related_id)
    response = r.get(query, headers=headers)

    return json.loads(response.text)
