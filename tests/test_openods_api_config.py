import pytest


def test_app_hostname_is_not_none():
    from openods import app
    value = app.config['APP_HOSTNAME']
    assert value is not None


def test_cache_timeout_is_greater_equal_0():
    from openods import app
    value = app.config['CACHE_TIMEOUT']
    assert value >= 0


def test_database_url_is_not_none():
    from openods import app
    value = app.config['DATABASE_URL']
    assert value is not None
