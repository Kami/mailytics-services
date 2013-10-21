import httplib

from tornado.web import HTTPError, asynchronous
from tornado.gen import engine, Task

from token_storage_server.handlers.base import JsonRequestHandler
from token_storage_server.database import get_refresh_token_for_user
from token_storage_server.utils import get_new_access_token

__all__ = [
    'AccessTokenHandler',
]


class AccessTokenHandler(JsonRequestHandler):
    @asynchronous
    @engine
    def get(self, account_uuid):
        refresh_token = get_refresh_token_for_user(account_uuid=account_uuid)

        if not refresh_token:
            raise HTTPError(status_code=httplib.NOT_FOUND,
                            log_message='Token not found')

        # TODO: Prevent thundering herd from multiple requests
        result = yield Task(get_new_access_token, refresh_token=refresh_token)

        data = {'access_token': result['access_token']}
        self.write_json(data, status_code=httplib.OK)
