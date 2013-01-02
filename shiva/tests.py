# -*- coding: utf-8 -*-
import unittest
from shiva.api.app import app as shiva


class ShivaTestCase(unittest.TestCase):
    """
    Test:
        Return codes: 200, 404 and 405
        Structures
        Data
    """
    def setUp(self):
        self.db_fd, shiva.config['DATABASE'] = tempfile.mkstemp()
        shiva.config['TESTING'] = True
        self.app = shiva.test_client()
        shiva.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(shiva.config['DATABASE'])

    def test_tracks(self):
        pass

if __name__ == '__main__':
    unittest.main()
