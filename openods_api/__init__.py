from flask import Flask
from openods_api.database import schema_check

__version__ = '0.2'
target_schema_version = '004'

schema_check.check_schema_version(target_schema_version)

app = Flask(__name__)

import openods_api.routes
