import logging
import sys
from urllib.parse import urlparse as urlparse

import psycopg2
import psycopg2.extras
import psycopg2.pool

from openods import app

log = logging.getLogger('openods')


url = urlparse(app.config['DATABASE_URL'])


def get_connection():
    try:
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        log.debug("Connected to {db_url}".format(db_url=app.config['DATABASE_URL']))

    except psycopg2.Error as e:
        log.warning("Unable to connect to the database on {db_url}".format(db_url=app.config['DATABASE_URL']))
        sys.exit(1)

    return conn


def get_cursor():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return cur