import sys

import logging
from urllib.parse import urlparse as urlparse

import config as config
import psycopg2
import psycopg2.extras
import psycopg2.pool

log = logging.getLogger('openods')


url = urlparse(config.DATABASE_URL)


def get_connection():
    try:
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        log.info("Connected to database")

    except psycopg2.Error as e:
        log.warning("I am unable to connect to the database")
        sys.exit(1)

    return conn


def get_cursor():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return cur