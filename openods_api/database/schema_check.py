import psycopg2, psycopg2.extras
from urllib.parse import urlparse as urlparse
import logging
import openods_api.config as config
import sys

log = logging.getLogger('openods')

url = urlparse(config.DATABASE_URL)


def check_schema_version():
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
        log.error("Unable to connect to the database")
        sys.exit(1)

    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        sql = "SELECT value from settings WHERE key = 'schema_version';"
        cur.execute(sql)
        result = cur.fetchone()
        db_schema_version = result['value']

    except TypeError as e:
        log.error("Unable to read schema version from the database")
        log.error("Exception: %s" % e)
        sys.exit(1)

    except psycopg2.Error as e:
        log.error("Error retrieving schema_version from database")
        raise

    if not (config.TARGET_SCHEMA_VERSION == db_schema_version):
        raise RuntimeError(str.format("Incorrect database schema version. Wanted {0}, Got {1}",
                                      config.TARGET_SCHEMA_VERSION, db_schema_version))

    else:
        log.info(str.format("Database schema version is {0}", db_schema_version))

    return True
