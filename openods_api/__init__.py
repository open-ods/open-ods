from flask import Flask

__version__ = '0.2'

app = Flask(__name__)

import openods_api.routes
