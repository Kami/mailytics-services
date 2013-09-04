import time
import httplib

from tornado.web import HTTPError, asynchronous
from tornado.gen import engine, Task

from token_storage_server.handlers.base import JsonRequestHandler
from token_storage_server.database import get_refresh_token_for_user
from token_storage_server.database import get_access_token_for_user
from token_storage_server.database import update_user_access_token

from token_storage_server.utils import get_new_access_token

__all__ = [
    'AccessTokenHandler',
]

# For how long should token still be active so we consider it as valid
TOKEN_THRESHOLD_SECONDS = 10 * 60


class AccessTokenHandler(JsonRequestHandler):
    @asynchronous
    @engine
    def get(self, user_id):
        refresh_token = get_refresh_token_for_user(user_id=user_id)

        if not refresh_token:
            raise HTTPError(status_code=httplib.NOT_FOUND,
                            log_message='Token not found')

        # TODO: Prevent thundering herd from multiple requests
        now = time.time()
        threshold_time = now - TOKEN_THRESHOLD_SECONDS
        access_token = get_access_token_for_user(user_id=user_id,
                                                 expires_threshold=threshold_time)

        if access_token:
            data = {'access_token': access_token}
            self.write_json(data, status_code=httplib.OK)
            return

        # Access token is not present or expired, we need to request a new one
        result = yield Task(get_new_access_token, refresh_token)

        # Cache new access token
        update_user_access_token(user_id=user_id,
                                 access_token=result['access_token'],
                                 expires_at=result['expires_at'])

        data = {'access_token': result['access_token']}
        self.write_json(result, status_code=httplib.OK)
