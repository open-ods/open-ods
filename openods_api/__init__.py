from flask import Flask

app = Flask(__name__)

from openods_api import routes

