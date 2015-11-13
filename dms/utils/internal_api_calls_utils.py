__author__ = 'asseym'

import base64
import json
import requests
from dms.models.token import Token
from necoc import settings

from dms.models import User
from mongoengine import DoesNotExist
from rest_framework import HTTP_HEADER_ENCODING


def post_to_api(api_endpoint, data_dict, auth='custom'):
    if auth =='custom':
        _post_with_custom_auth(api_endpoint, data_dict)
    elif auth =='basic':
        return _post_with_basic_auth(api_endpoint, data_dict)
    else:
        return _post_with_token_auth(api_endpoint, data_dict)


def _post_with_custom_auth(api_endpoint, data_dict):
    api_url = settings.HOSTNAME + api_endpoint
    data = json.dumps(data_dict)
    api_user = User.objects.order_by('-id').first()

    return requests.post(api_url, data, \
                         headers={'x-api-user': api_user.username, \
                                  'content-type': 'application/json'})


def _post_with_basic_auth(api_endpoint, data_dict):
    api_url = settings.HOSTNAME + api_endpoint
    data = json.dumps(data_dict)
    payload = {'username': 'api_user', 'password': settings.API_USER_PASS}
    api_user = User.objects.order_by('-id').first()
    if api_user is None:
        api_user = User(**dict(username=payload['username'], is_active=True)).save()
        api_user.set_password(payload['password'])
        basic_auth_key = _basic_auth_header(payload['username'], payload['password'])
    else:
        basic_auth_key = _basic_auth_header(api_user.username, settings.API_USER_PASS)

    return requests.post(api_url, data, \
                         headers={'Authorization': basic_auth_key, 'content-type': 'application/json'})


def _post_with_token_auth(api_endpoint, data_dict):
    api_url = settings.HOSTNAME + api_endpoint
    payload = {'username': 'api_user', 'password': settings.API_USER_PASS}
    api_user = User.objects.order_by('-id').first()
    if api_user is None:
        api_user = User(**dict(username=payload['username'], is_active=True)).save()
        api_user.set_password(payload['password'])

        token, created = Token.objects.get_or_create(user=api_user)
    else:
        try:
            token = Token.objects.get(user=api_user)
        except DoesNotExist:
            token, created = Token.objects.get_or_create(user=api_user)

    return requests.post(api_url, json.dumps(data_dict), \
                  headers={'Authorization': 'Token %s' % token.key, 'content-type': 'application/json'})


def _basic_auth_header(username, password):
    credentials = ('%s:%s' % (username, password))
    base64_credentials = base64.b64encode(credentials.encode(HTTP_HEADER_ENCODING)).decode(HTTP_HEADER_ENCODING)
    print base64_credentials
    return 'Basic %s' % base64_credentials