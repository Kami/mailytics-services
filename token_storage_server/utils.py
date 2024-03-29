import json
import time
import httplib
from urllib import urlencode

from tornado.options import options
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.gen import Task, engine

TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
CLIENT_SECRETS = None


def get_secret(key):
    global CLIENT_SECRETS

    if not CLIENT_SECRETS:
        with open(options.secrets_path) as fp:
            data = fp.read()

        CLIENT_SECRETS = json.loads(data)['web']

    return CLIENT_SECRETS[key]


@engine
def get_new_access_token(refresh_token, callback):
    """
    Hit Google API with the provided refresh token and retrieves a new access
    token.

    Return a ``dict`` with access_token and expires_at key.
    """
    client_id = get_secret('client_id')
    client_secret = get_secret('client_secret')

    payload = {'refresh_token': refresh_token, 'client_id': client_id,
               'client_secret': client_secret, 'grant_type': 'refresh_token'}
    payload = urlencode(payload)

    client = AsyncHTTPClient()
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    request = HTTPRequest(url=TOKEN_URI, method='POST', body=payload,
                          headers=headers)
    response = yield Task(client.fetch, request)

    if response.code != httplib.OK:
        raise Exception('Code: %s, Error: %s' % (response.code, response.body))
        return

    now = time.time()
    data = json.loads(response.body)
    expires_at = now + data['expires_in']
    result = {'access_token': data['access_token'], 'expires_at': expires_at}
    callback(result)
