from token_storage.handlers.refresh_token import RefreshTokenHandler


urls = [
    (r'/users/(\w+)/refresh_token', RefreshTokenHandler)
]
