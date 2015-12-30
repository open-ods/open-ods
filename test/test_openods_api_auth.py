import unittest
from openods_core import app
import openods_core.auth as auth


class AuthTests(unittest.TestCase):

    def test_check_auth_returns_false_for_invalid_credentials(self):
        self.assertFalse(auth.check_auth('incorrect_user', 'incorrect_password'))

    def test_check_auth_returns_true_for_valid_credentials(self):
        self.assertTrue(auth.check_auth('env_test_user','env_test_pass'))


class RouteAuthTests(unittest.TestCase):

    def test_organisations_request_with_no_auth_returns_403_response(self):
        tester = app.test_client(self)
        response = tester.get('/organisations/', content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_organisations_search_request_with_no_auth_returns_403_response(self):
        tester = app.test_client(self)
        response = tester.get('/organisations/search/test/', content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_organisations_single_request_with_no_auth_returns_403_response(self):
        tester = app.test_client(self)
        response = tester.get('/organisations/RFF/', content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_roles_request_with_no_auth_returns_403_response(self):
        tester = app.test_client(self)
        response = tester.get('/role-types/', content_type='application/json')
        self.assertEqual(response.status_code, 401)