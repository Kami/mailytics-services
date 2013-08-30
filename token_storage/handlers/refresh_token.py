from tornado.web import RequestHandler

__all__ = [
    'RefreshTokenHandler'
]


class RefreshTokenHandler(RequestHandler):
    def get(self, user_id):
        self.write('Hello, world')

    def post(self, user_id):
        self.write('POST')
