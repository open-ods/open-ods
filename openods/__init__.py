__version__ = '0.16'

import logging
import re

# Import flask
from flask import Flask
from flask_cors import CORS
from flask_featureflags import FeatureFlag

# Define the WSGI application object
app = Flask(__name__)
feature_flags = FeatureFlag(app)

# Load the app configuration from the default_config.py file
app.config.from_object('openods.default_config')

# We check the version of the database schema that is available to the app
from openods import schema_check

schema_check.check_schema_version()

from openods import routes

# Set up logging
log_format = "%(asctime)s|OpenODS|%(levelname)s|%(message)s"
formatter = logging.Formatter(log_format)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) if app.config["DEBUG"] is True else logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.debug("Logging at DEBUG level")

# Allow Cross Origin Resource Sharing for routes under the API path so that other services can use the API
regEx = re.compile(app.config['API_PATH'] + "/*")
CORS(app, resources={regEx: {"origins": "*"}})
