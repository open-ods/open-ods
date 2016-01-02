import logging
import urllib.parse
from flask.ext.cacheify import init_cacheify

from app.openods_core import app
from flask import request

log = logging.getLogger('openods')

cache = init_cacheify(app)


def generate_cache_key():
    args = request.args
    key = request.path + '?' + urllib.parse.urlencode([
        (k, v) for k in sorted(args) for v in sorted(args.getlist(k))
    ])
    log.debug(str.format("Cache Key: {0}", key))
    return key
