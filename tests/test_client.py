import os
import sys
import unittest
from os.path import join as pjoin

from token_storage_client import GetClient, SetClient
from token_storage_client.errors import UserDoesNotExist

THIS_DIR = os.path.abspath(os.path.split(__file__)[0])


class ClientTestCase(unittest.TestCase):
    def setUp(self):
        client_cert = pjoin(THIS_DIR, '../fixtures/client/certs/client1.crt')
        client_key = pjoin(THIS_DIR, '../fixtures/client/keys/client1.key')
        ca_certs = pjoin(THIS_DIR, '../fixtures/ca/myCA.crt')

        kwargs = {'client_cert': client_cert, 'client_key': client_key,
                  'ca_certs': ca_certs}

        self.get_client = GetClient(server_urls=['https://localhost:8888'], **kwargs)
        self.set_client = SetClient(server_urls=['https://localhost:8889'], **kwargs)

    def test_get_doesnt_exist(self):
        self.assertRaises(UserDoesNotExist, self.get_client.get, user_id='inexistent')

if __name__ == '__main__':
    sys.exit(unittest.main())
