__version__ = '0.13b'

import logging
import re
import config as config

# Import flask and template operators
from flask import Flask
from flask_featureflags import FeatureFlag
from flask_cors import CORS

# Define the WSGI application object
app = Flask(__name__)
feature_flags = FeatureFlag(app)

# Configurations
app.config.from_object('config')

# Set up logging
log_format = "%(asctime)s %(levelname)s %(message)s"
formatter = logging.Formatter(log_format)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) if app.config["DEBUG"] is True else logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

# Allow Cross Origin Resource Sharing for routes under /api/ so that other services can use the data from the API
regEx=re.compile(config.API_URL+"/*")
CORS(app, resources={regEx: {"origins": "*"}})

# Import a module / component using its blueprint handler variable (mod_auth)
from app.openods_site.controllers import mod_site as site_module
from app.openods_core import routes

# Register blueprints
app.register_blueprint(site_module)


