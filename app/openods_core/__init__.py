import logging
from app import app
from flask.ext.cors import CORS

from flask import Flask

__version__ = '0.3'

log = logging.getLogger('openods')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)

# app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

