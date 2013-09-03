import os
import sys
import unittest
from os.path import join as pjoin

import requests
from requests.exceptions import SSLError

THIS_DIR = os.path.abspath(os.path.split(__file__)[0])


class ServerTestCase(unittest.TestCase):
    def setUp(self):
        self.url = 'https://localhost:8888/users/user1/refresh_token'
        self.client_cert = pjoin(THIS_DIR,
                                 '../fixtures/client/certs/client1.crt')
        self.client_key = pjoin(THIS_DIR,
                                '../fixtures/client/keys/client1.key')
        self.ca_certs = pjoin(THIS_DIR, '../fixtures/ca/myCA.crt')

    def test_missing_client_cert_and_invalid_ca(self):
        self.assertRaisesRegexp(SSLError, 'certificate verify failed',
                                requests.get, self.url)

    def test_no_client_cert_valid_ca_cert_provided(self):
        self.assertRaisesRegexp(SSLError, 'sslv3 alert handshake failure',
                                requests.get, self.url, verify=self.ca_certs)

    def test_valid_client_cert_missing_ca(self):
        cert = (self.client_cert, self.client_key)
        self.assertRaisesRegexp(SSLError, 'certificate verify failed',
                                requests.get, self.url, cert=cert)

    def test_invalid_client_cert_valid_ca_cert_provided(self):
        client_cert = pjoin(THIS_DIR, '../fixtures/dummy/waipio.ca.cert')
        client_key = pjoin(THIS_DIR, '../fixtures/dummy/waipio.ca.key')
        cert = (client_cert, client_key)
        self.assertRaisesRegexp(SSLError, 'tlsv1 alert unknown ca',
                                requests.get, self.url, verify=self.ca_certs,
                                cert=cert)

    def test_valid_cert_and_ca(self):
        cert = (self.client_cert, self.client_key)
        response = requests.get(self.url, cert=cert, verify=self.ca_certs)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    sys.exit(unittest.main())
