import logging
from app import app
from flask_cors import CORS

log = logging.getLogger('openods')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)

CORS(app, resources={r"/api/*": {"origins": "*"}})

