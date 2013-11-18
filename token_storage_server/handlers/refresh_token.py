import httplib

from tornado.web import HTTPError
from tornado.options import options
from hybrid_crypto.crypto import HybridCryptoDecrypter

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

        decrypter = HybridCryptoDecrypter(keys_path=options.private_keys_path)
        refresh_token = decrypter.decrypt(data=refresh_token)

        data = {'refresh_token': refresh_token}
        self.write_json(data, status_code=201)


class RefreshTokenSetHandler(JsonRequestHandler):
    def put(self, account_uuid):
        """
        Store an encrypted refresh token for the provided account.
        """
        data = self.parse_json()
        refresh_token = data['refresh_token']

        valid = self._is_refresh_token_valid(refresh_token=refresh_token)

        if not valid:
            raise HTTPError(status_code=httplib.BAD_REQUEST,
                            log_message='Refresh token is not valid')

        update_user_refresh_token(account_uuid=account_uuid,
                                  refresh_token=refresh_token)
        self.set_status(status_code=httplib.NO_CONTENT)

    def delete(self, account_uuid):
        """
        Delete a refresh token for the provided account.
        """
        delete_user_refresh_token(account_uuid=account_uuid)
        self.set_status(status_code=httplib.NO_CONTENT)

    def _is_refresh_token_valid(self, refresh_token):
        """
        Validate that the provided refresh token is encrypted using a
        recognized scheme.
        """
        if not refresh_token:
            return False

        if refresh_token.startswith('hpkc'):
            return True

        return False
