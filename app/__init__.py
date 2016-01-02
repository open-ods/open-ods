__version__ = '0.4'

import logging

# Import flask and template operators
from flask import Flask, render_template
from flask.ext.cors import CORS

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

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

# app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.openods_site.controllers import mod_site as site_module
from app.openods_core import routes

# Register blueprint(s)
app.register_blueprint(site_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
