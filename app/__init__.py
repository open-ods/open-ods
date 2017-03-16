__version__ = '0.11'

import logging
import re
import config as config

# Import flask and template operators
from flask import Flask, render_template
from flask_featureflags import FeatureFlag
from flask_cors import CORS

# Define the WSGI application object
app = Flask(__name__)
feature_flags = FeatureFlag(app)

# Configurations
app.config.from_object('config')

# Set up logging
log = logging.getLogger('openods')
# log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Add the handlers to the logger
log.addHandler(ch)

# Allow Cross Origin Resource Sharing for routes under /api/ so that other services can use the data from the API
regEx=re.compile(config.API_URL+"/*")
CORS(app, resources={regEx: {"origins": "*"}})


# HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.openods_site.controllers import mod_site as site_module
from app.openods_core import routes

# Register blueprints
app.register_blueprint(site_module)


