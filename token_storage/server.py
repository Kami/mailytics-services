import ssl

from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from token_storage.urls import urls


def run_server():
    application = Application(urls, debug=True)
    ssl_options = dict(
        certfile='fixtures/server/certs/server.crt',
        keyfile='fixtures/server/keys/server.key',
        ca_certs='fixtures/ca/myCA.crt',
        cert_reqs=ssl.CERT_REQUIRED,
    )

    server = HTTPServer(application, ssl_options=ssl_options)
    server.listen(8888)
    IOLoop.instance().start()

if __name__ == '__main__':
    run_server()
