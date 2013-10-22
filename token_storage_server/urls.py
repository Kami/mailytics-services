from token_storage_server.handlers.refresh_token import RefreshTokenGetHandler
from token_storage_server.handlers.refresh_token import RefreshTokenSetHandler
from token_storage_server.handlers.access_token import AccessTokenHandler


__all__ = [
    'get_urls',
    'set_urls'
]

get_urls = [
    (r'/accounts/(?P<account_uuid>.+?)/refresh_token', RefreshTokenGetHandler),
    (r'/accounts/(?P<account_uuid>.+?)/access_token', AccessTokenHandler)
]

set_urls = [
    (r'/accounts/(?P<account_uuid>.+?)/refresh_token', RefreshTokenSetHandler)
]
