__all__ = [
    'UserDoesNotExist'
]


class UserDoesNotExist(Exception):
    def __init__(self, user_id):
        self.user_id = user_id
        self.message = 'User %s does not exist' % (self.user_id)
