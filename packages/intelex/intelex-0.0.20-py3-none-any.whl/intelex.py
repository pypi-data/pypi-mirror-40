import requests as r
import os
import json


def get_version():
    return '0.0.20'


def get_records(object):
    ilx_endpoint = os.environ['ilx_endpoint']
    ilx_apikey = os.environ['ilx_apikey']
    auth_header = 'Basic {}'.format(ilx_apikey)

    headers = {
        'Authorization': auth_header
    }

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

    query = '{}/api/v2/object/{}({})/{}({})'.format(ilx_endpoint, object, id, navigation_property, related)
    response = r.get(query, headers=headers)

    return json.loads(response.text)
