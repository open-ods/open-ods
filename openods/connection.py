import logging
import sys
from urllib.parse import urlparse as urlparse

import psycopg2
import psycopg2.extras
import psycopg2.pool

import sqlalchemy.pool as pool
from sqlalchemy import event
from flask import g

from openods import app

url = urlparse(app.config['DATABASE_URL'])


def get_new_conn():
    try:
        logger = logging.getLogger(__name__)
        logger.debug("Getting new connection")
        c = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
        return c
    
    except psycopg2.Error as e:
        logger.critical("Unable to connect to the database on {db_url}".format(db_url=app.config['DATABASE_URL']),
                        exc_info=True)
        sys.exit(1)


def get_connection():
    conn = my_pool.connect()
    logger = logging.getLogger(__name__)
    logger.debug('requestId="{request_id}"|Getting connection from pool'.format(request_id=g.request_id))
    return conn


def get_cursor():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    logger = logging.getLogger(__name__)
    logger.debug('requestId="{request_id}"|Getting cursor'.format(request_id=g.request_id))
    return cur


def my_on_checkin(dbapi_conn, connection_rec):
    logger = logging.getLogger(__name__)
    logger.debug('requestId="{request_id}"|Connection checkin'.format(request_id=g.request_id))


def my_on_checkout(dbapi_conn, connection_rec, connection_proxy):
    logger = logging.getLogger(__name__)
    logger.debug('requestId="{request_id}"|Connection checkout'.format(request_id=g.request_id))

# Create a connection pool
my_pool = pool.QueuePool(get_new_conn, max_overflow=10, pool_size=5)

# If the app is running in DEBUG mode, put an event listener to trigger on checkin / checkout from the pool
if app.config['DEBUG']:
    logger = logging.getLogger(__name__)
    logger.debug("Adding event listeners for connection pool checkin / checkout")
    event.listen(my_pool, 'checkin', my_on_checkin)
    event.listen(my_pool, 'checkout', my_on_checkout)