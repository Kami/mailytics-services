#!/usr/bin/env python
from tornado.options import define

from token_storage_server.server import run_server
from token_storage_server.urls import get_urls

define('port', default=7979,
       help='Port to listen on')

if __name__ == '__main__':
    run_server(urls=get_urls)
