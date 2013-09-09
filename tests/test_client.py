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

        self.get_client = GetClient(server_urls=['https://localhost:8888'],
                                    **kwargs)
        self.set_client = SetClient(server_urls=['https://localhost:9999'],
                                    **kwargs)

    def test_get_refresh_token_doesnt_exist(self):
        self.assertRaises(UserDoesNotExist, self.get_client.get_refresh_token,
                          user_id='inexistent')

    def test_get_access_token_doesnt_exist(self):
        self.assertRaises(UserDoesNotExist, self.get_client.get_access_token,
                          user_id='inexistent')

    def test_set(self):
        self.assertRaises(UserDoesNotExist, self.get_client.get_refresh_token,
                          user_id='user1')

        # get_refresh_token
        self.assertTrue(self.set_client.set('user1', 'footoken1'))

        token = self.get_client.get_refresh_token('user1')
        self.assertEqual(token, 'footoken1')
        self.assertTrue(self.set_client.set('user1', 'footoken2'))

        token = self.get_client.get_refresh_token('user1')
        self.assertEqual(token, 'footoken2')

        # get_access_token
        # TODO: mock google api server url

    def test_delete(self):
        self.assertRaises(UserDoesNotExist, self.get_client.get_refresh_token,
                          user_id='user2')

        self.assertTrue(self.set_client.delete('user2'))
        self.assertTrue(self.set_client.set('user2', 'footoken2'))
        token = self.get_client.get_refresh_token('user2')
        self.assertEqual(token, 'footoken2')
        self.assertTrue(self.set_client.delete('user2'))
        self.assertRaises(UserDoesNotExist, self.get_client.get_refresh_token,
                          user_id='user2')

if __name__ == '__main__':
    sys.exit(unittest.main())
