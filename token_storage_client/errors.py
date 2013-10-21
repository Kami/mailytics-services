__all__ = [
    'UserDoesNotExist'
]


class UserDoesNotExist(Exception):
    def __init__(self, account_uuid):
        self.account_uuid = account_uuid
        self.message = 'Account %s does not exist' % (self.account_uuid)
