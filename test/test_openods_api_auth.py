import unittest
import openods_api.auth as auth


class AuthTests(unittest.TestCase):

    def test_check_auth_returns_false_for_invalid_credentials(self):
        self.assertFalse(auth.check_auth('incorrect_user', 'incorrect_password'))

    def test_check_auth_returns_true_for_valid_credentials(self):
        self.assertTrue(auth.check_auth('env_test_user','env_test_pass'))
