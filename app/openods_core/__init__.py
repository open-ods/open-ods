import re
import config as config
from app import app
from flask_cors import CORS

regEx=re.compile(config.API_URL+"/*")
CORS(app, resources={regEx: {"origins": "*"}})
