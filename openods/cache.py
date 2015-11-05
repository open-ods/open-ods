import urllib.parse
from flask import request
from openods import app
from flask.ext.cacheify import init_cacheify

cache = init_cacheify(app)


def generate_cache_key():
    args = request.args
    key = request.path + '?' + urllib.parse.urlencode([
        (k, v) for k in sorted(args) for v in sorted(args.getlist(k))
    ])
    print(key)
    return key
