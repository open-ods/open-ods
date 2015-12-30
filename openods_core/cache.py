import urllib.parse
import logging
from flask import request
from openods_core import app
from flask.ext.cacheify import init_cacheify

log = logging.getLogger('openods')

cache = init_cacheify(app)


def generate_cache_key():
    args = request.args
    key = request.path + '?' + urllib.parse.urlencode([
        (k, v) for k in sorted(args) for v in sorted(args.getlist(k))
    ])
    log.debug(str.format("Cache Key: {0}", key))
    return key
