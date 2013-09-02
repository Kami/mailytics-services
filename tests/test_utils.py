import sys
import unittest

from token_storage_client.utils import retry_on_error


class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.i = 0

    def test_retry_on_error(self):
        # No exception
        self.i = 0

        @retry_on_error(retry_count=3)
        def func():
            self.i += 1
            pass

        func()
        self.assertEqual(self.i, 1)

        # Uncaught exception
        self.i = 0

        @retry_on_error(retry_count=3, exceptions=(ValueError))
        def func():
            raise IndexError(0)

        self.assertRaises(IndexError, func)

        # Caught parent exception with success
        self.i = 0

        @retry_on_error(retry_count=3, exceptions=(Exception), delay=0.1)
        def func():
            self.i += 1
            if self.i < 2:
                raise IndexError(0)

        func()
        self.assertEqual(self.i, 2)

        # Caught sub exception with success
        self.i = 0

        @retry_on_error(retry_count=3, exceptions=(IndexError), delay=0.1)
        def func():
            self.i += 1
            if self.i < 2:
                raise IndexError(0)

        func()
        self.assertEqual(self.i, 2)

        # Retried, but didn't success
        self.i = 0

        @retry_on_error(retry_count=3, exceptions=(IndexError), delay=0.1)
        def func():
            self.i += 1
            raise IndexError(0)

        self.assertRaises(IndexError, func)
        self.assertEqual(self.i, 3)

if __name__ == '__main__':
    sys.exit(unittest.main())
