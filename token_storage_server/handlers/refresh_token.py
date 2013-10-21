import httplib

from tornado.web import HTTPError

from token_storage_server.handlers.base import JsonRequestHandler
from token_storage_server.database import get_refresh_token_for_user
from token_storage_server.database import update_user_refresh_token
from token_storage_server.database import delete_user_refresh_token

__all__ = [
    'RefreshTokenGetHandler',
    'RefreshTokenSetHandler',
]


class RefreshTokenGetHandler(JsonRequestHandler):
    def get(self, account_uuid):
        refresh_token = get_refresh_token_for_user(account_uuid=account_uuid)

        if not refresh_token:
            raise HTTPError(status_code=httplib.NOT_FOUND,
                            log_message='Token not found')

        data = {'refresh_token': refresh_token}
        self.write_json(data, status_code=201)


class RefreshTokenSetHandler(JsonRequestHandler):
    def put(self, account_uuid):
        data = self.parse_json()
        # TODO: validate
        refresh_token = data['refresh_token']

        update_user_refresh_token(account_uuid=account_uuid,
                                  refresh_token=refresh_token)
        self.set_status(status_code=httplib.NO_CONTENT)

    def delete(self, account_uuid):
        delete_user_refresh_token(account_uuid=account_uuid)
        self.set_status(status_code=httplib.NO_CONTENT)
