from token_storage_server.handlers.refresh_token import RefreshTokenHandler


urls = [
    (r'/users/(\w+)/refresh_token', RefreshTokenHandler)
]
