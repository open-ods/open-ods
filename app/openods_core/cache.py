import logging
import urllib.parse
from flask_cacheify import init_cacheify

from app.openods_core import app
from flask import request

cache = init_cacheify(app)


def generate_cache_key():

    logger = logging.getLogger(__name__)

    args = request.args
    key = request.path + '?' + urllib.parse.urlencode([
        (k, v) for k in sorted(args) for v in sorted(args.getlist(k))
    ])

    logger.debug(str.format("CacheKey:{0}", key))

    return key
