from token_storage_server.handlers.refresh_token import RefreshTokenGetHandler
from token_storage_server.handlers.refresh_token import RefreshTokenSetHandler


__all__ = [
    'get_urls',
    'set_urls'
]

get_urls = [
    (r'/users/(\w+)/refresh_token', RefreshTokenGetHandler)
]

set_urls = [
    (r'/users/(\w+)/refresh_token', RefreshTokenSetHandler)
]
