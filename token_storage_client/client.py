import random
import httplib
import json

import requests
from requests.exceptions import ConnectionError

from token_storage_client.utils import method_decorator, retry_on_error
from token_storage_client.errors import UserDoesNotExist


class BaseClient(object):
    def __init__(self, server_urls, client_cert, client_key, ca_certs):
        self._server_urls = server_urls
        self._client_cert = client_cert
        self._client_key = client_key
        self._ca_certs = ca_certs

        self._cert_arg = (self._client_cert, self._client_key)
        self._verify_arg = self._ca_certs


class GetClient(BaseClient):
    @method_decorator(retry_on_error(retry_count=3,
                                     exceptions=(ConnectionError,)))
    def get(self, user_id):
        url = random.choice(self._server_urls)
        values = {'url': url, 'user_id': user_id}
        url = '%(url)s//users/%(user_id)s/refresh_token' % values
        response = requests.get(url, cert=self._cert_arg,
                                verify=self._verify_arg)

        if response.status_code == httplib.NOT_FOUND:
            raise UserDoesNotExist(user_id=user_id)

        data = response.json()
        return data['refresh_token']


class SetClient(BaseClient):
    @method_decorator(retry_on_error(retry_count=3,
                      exceptions=(ConnectionError,)))
    def set(self, user_id, refresh_token):
        # TODO: This method should try to re-try
        url = random.choice(self._server_urls)
        values = {'url': url, 'user_id': user_id}
        url = '%(url)s//users/%(user_id)s/refresh_token' % values
        data = json.dumps({'refresh_token': refresh_token})

        response = requests.put(url, data=data, cert=self._cert_arg,
                                verify=self._verify_arg)
        if response.status_code != httplib.NO_CONTENT:
            raise Exception('Failed to save refresh token: %s' %
                            (response.body))

        return True
