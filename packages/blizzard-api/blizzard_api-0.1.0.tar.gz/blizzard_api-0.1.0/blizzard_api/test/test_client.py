
"""
Blizzard API CLI - TestClient class.

Vaughn Kottler 01/07/19
"""

# built-in
import unittest

# internal
from blizzard_api.test.resources import get_item

# payload
from blizzard_api.client import main

class TestClient(unittest.TestCase):
    """ Testing the application entry-point. """

    def setUp(self):
        """ Declare default application arguments. """

        self.args = ["dummy", "-a"]

    def test_nominal_credentials(self):
        """ Validate that a good credentials file can be parsed. """

        self.assertEqual(main(self.args + [get_item("good_cred_file.json")]), 0)

    def test_bad_credentials(self):
        """ Validate that bad credentials files can't be parsed. """

        self.assertEqual(main(self.args + [get_item("bad_cred_file1.json")]), 1)
        self.assertEqual(main(self.args + [get_item("bad_cred_file2.json")]), 1)
        self.assertEqual(main(self.args + [get_item("bad_cred_file3.json")]), 1)
        self.assertEqual(main(self.args + [get_item("bad_cred_file4.json")]), 1)
