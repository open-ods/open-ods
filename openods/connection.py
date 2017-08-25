import logging
import sys
from urllib.parse import urlparse as urlparse

import psycopg2
import psycopg2.extras
import psycopg2.pool
from flask import g

from openods import app

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
        
        logger = logging.getLogger(__name__)
        logger.debug('requestId="{request_id}"|Connected to {db_url}'.format(db_url=app.config['DATABASE_URL'],
                                                                             request_id=g.request_id))
    
    except psycopg2.Error:
        logger = logging.getLogger(__name__)
        logger.critical("Unable to connect to the database on {db_url}".format(db_url=app.config['DATABASE_URL']))
        sys.exit(1)
    
    return conn


def get_cursor():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return cur
