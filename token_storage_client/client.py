import random
import httplib
import json

import requests
from requests.exceptions import ConnectionError

from token_storage_client.utils import method_decorator, retry_on_error
from token_storage_client.errors import UserDoesNotExist


class BaseClient(object):
    def __init__(self, server_urls, client_cert, client_key, ca_certs):
        self._server_urls = self._normalize_urls(urls=server_urls)
        self._client_cert = client_cert
        self._client_key = client_key
        self._ca_certs = ca_certs

        self._cert_arg = (self._client_cert, self._client_key)
        self._verify_arg = self._ca_certs

    def _normalize_urls(self, urls):
        """
        Normalize server URLs (remove trailing slash).
        """
        result = []

        for url in urls:
            if url.endswith('/'):
                url = url[:-1]

            result.append(url)

        return result


class GetClient(BaseClient):
    @method_decorator(retry_on_error(retry_count=3,
                                     exceptions=(ConnectionError,)))
    def get_access_token(self, account_uuid):
        url = random.choice(self._server_urls)
        values = {'url': url, 'account_uuid': account_uuid}
        url = '%(url)s/users/%(account_uuid)s/access_token' % values
        response = requests.get(url, cert=self._cert_arg,
                                verify=self._verify_arg)

        if response.status_code == httplib.NOT_FOUND:
            raise UserDoesNotExist(account_uuid=account_uuid)

        data = response.json()
        return data['access_token']

    @method_decorator(retry_on_error(retry_count=3,
                                     exceptions=(ConnectionError,)))
    def get_refresh_token(self, account_uuid):
        url = random.choice(self._server_urls)
        values = {'url': url, 'account_uuid': account_uuid}
        url = '%(url)s/users/%(account_uuid)s/refresh_token' % values
        response = requests.get(url, cert=self._cert_arg,
                                verify=self._verify_arg)

        if response.status_code == httplib.NOT_FOUND:
            raise UserDoesNotExist(account_uuid=account_uuid)

        data = response.json()
        return data['refresh_token']


class SetClient(BaseClient):
    @method_decorator(retry_on_error(retry_count=3,
                      exceptions=(ConnectionError,)))
    def set_refresh_token(self, account_uuid, refresh_token):
        url = random.choice(self._server_urls)
        values = {'url': url, 'account_uuid': account_uuid}
        url = '%(url)s/users/%(account_uuid)s/refresh_token' % values
        data = json.dumps({'refresh_token': refresh_token})

        response = requests.put(url, data=data, cert=self._cert_arg,
                                verify=self._verify_arg)
        if response.status_code != httplib.NO_CONTENT:
            raise Exception('Failed to save refresh token: %s' %
                            (response.text))

        return True

    @method_decorator(retry_on_error(retry_count=3,
                      exceptions=(ConnectionError,)))
    def delete(self, account_uuid):
        url = random.choice(self._server_urls)
        values = {'url': url, 'account_uuid': account_uuid}
        url = '%(url)s/users/%(account_uuid)s/refresh_token' % values

        response = requests.delete(url, cert=self._cert_arg,
                                   verify=self._verify_arg)
        if response.status_code != httplib.NO_CONTENT:
            raise Exception('Failed to delete refresh token: %s' %
                            (response.text))

        return True
