__version__ = '0.2'

from flask import Flask

app = Flask(__name__)

from openods_api import routes

