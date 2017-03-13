import logging
import re
import config as config
from app import app
from flask_cors import CORS

log = logging.getLogger('openods')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)

regEx=re.compile(config.API_URL+"/*")
CORS(app, resources={regEx: {"origins": "*"}})

