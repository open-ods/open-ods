import urllib.parse
import logging
from flask import request
from openods import app
from flask.ext.cacheify import init_cacheify

log = logging.getLogger('openods')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)

cache = init_cacheify(app)


def generate_cache_key():
    args = request.args
    key = request.path + '?' + urllib.parse.urlencode([
        (k, v) for k in sorted(args) for v in sorted(args.getlist(k))
    ])
    log.debug(str.format("Cache Key: {0}", key))
    return key
