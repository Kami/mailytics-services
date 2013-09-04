import os
import ssl
import logging

from tornado.options import define, options
from tornado.options import parse_command_line
from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

__all__ = [
    'run_server'
]

logger = logging.getLogger()

define('cert_file', default='fixtures/server/certs/server.crt',
       help='Path to the server certificate file')
define('key_file', default='fixtures/server/keys/server.key',
       help='Path to the server certificate key file')
define('ca_file', default='fixtures/ca/myCA.crt',
       help='Path to the CA file')
define('database_path', default='database.sqlite',
       help='Path to the database file')


def run_server(urls):
    parse_command_line()

    if not os.path.exists(options.database_path):
        raise ValueError('Database file doesn\'t exist')

    if options.secrets_path and not os.path.exists(options.secrets_path):
        raise ValueError('secrets_path file doesn\'t exist')

    debug = options.logging == 'debug'
    application = Application(urls, debug=debug)
    ssl_options = dict(
        certfile=options.cert_file,
        keyfile=options.key_file,
        ca_certs=options.ca_file,
        cert_reqs=ssl.CERT_REQUIRED,
    )

    server = HTTPServer(application, ssl_options=ssl_options)
    server.listen(options.port)
    logging.info('Server listening on %(port)s' % {'port': options.port})
    IOLoop.instance().start()
