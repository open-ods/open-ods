import os

TARGET_SCHEMA_VERSION = '009'
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://openods:openods@localhost:5432/openods')
CACHE_TIMEOUT = int(os.environ.get('CACHE_TIMEOUT', '30'))
APP_HOSTNAME = os.environ.get('APP_HOSTNAME', 'localhost:5000/api')
API_USER = os.environ.get('API_USER', 'user')
API_PASS = os.environ.get('API_PASS', 'pass')
API_URL = os.environ.get('API_URL', '/api')
LIVE_DEPLOYMENT = os.environ.get('LIVE_DEPLOYMENT', 'FALSE')
INSTANCE_NAME = os.environ.get('INSTANCE_NAME', 'Development')

print(str.format("Database URL: {0}", DATABASE_URL))
print(str.format("Cache Timeout: {0}", CACHE_TIMEOUT))
print(str.format("App Hostname: {0}", APP_HOSTNAME))
print(str.format("App User: {0}", API_USER))
print(str.format("App Password: {0}", API_PASS))
print(str.format("API URL: {0}", API_URL))

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"