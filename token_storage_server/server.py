import ssl

from tornado.options import define, options
from tornado.options import parse_command_line
from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from token_storage_server.urls import urls

define('cert_file', default='fixtures/server/certs/server.crt',
       help='Path to the server certificate file')
define('key_file', default='fixtures/server/keys/server.key',
       help='Path to the server certificate key file')
define('ca_file', default='fixtures/ca/myCA.crt',
       help='Path to the CA file')


def run_server():
    parse_command_line()
    debug = options.logging == 'debug'
    application = Application(urls, debug=debug)
    ssl_options = dict(
        certfile=options.cert_file,
        keyfile=options.key_file,
        ca_certs=options.ca_file,
        cert_reqs=ssl.CERT_REQUIRED,
    )

    server = HTTPServer(application, ssl_options=ssl_options)
    server.listen(8888)
    IOLoop.instance().start()

if __name__ == '__main__':
    run_server()
