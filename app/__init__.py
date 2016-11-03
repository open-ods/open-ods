__version__ = '0.6'

import logging

# Import flask and template operators
from flask import Flask, render_template
from flask_cors import CORS

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Set up logging
log = logging.getLogger('openods')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)

CORS(app, resources={r"/api/*": {"origins": "*"}})


# HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.openods_site.controllers import mod_site as site_module
from app.openods_core import routes

# Register blueprints
app.register_blueprint(site_module)


