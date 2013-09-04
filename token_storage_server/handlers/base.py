import json
import httplib

from tornado.web import RequestHandler, HTTPError

__all__ = [
    'JsonRequestHandler'
]


class JsonRequestHandler(RequestHandler):
    def write_json(self, data, status_code=httplib.OK):
        self.set_header('Content-Type', 'application/json')
        self.set_status(status_code=status_code)
        data = json.dumps(data)
        self.finish(data)

    def parse_json(self):
        try:
            data = json.loads(self.request.body)
        except ValueError:
            raise HTTPError(status_code=httplib.BAD_REQUEST)

        return data
