from flask import Flask
from flask.ext.cors import CORS
import logging
__version__ = '0.3'

log = logging.getLogger('openods')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

import openods_api.routes
