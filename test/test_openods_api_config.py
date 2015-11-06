import unittest
import openods_api.config as config


class ConfigTests(unittest.TestCase):

    def test_app_hostname_is_not_none(self):
        value = config.APP_HOSTNAME
        self.assertIsNotNone(value)

    def test_cache_timeout_is_greater_equal_0(self):
        value = config.CACHE_TIMEOUT
        self.assertGreaterEqual(value, 0)

    def test_database_url_is_not_none(self):
        value = config.DATABASE_URL
        self.assertIsNotNone(value)
