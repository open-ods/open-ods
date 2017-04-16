import os

TARGET_SCHEMA_VERSION = '012'
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://openods:openods@localhost:5432/openods')
CACHE_TIMEOUT = int(os.environ.get('CACHE_TIMEOUT', '30'))
APP_HOSTNAME = os.environ.get('APP_HOSTNAME', 'http://localhost:5000/api')
API_PATH = os.environ.get('API_PATH', '/api')
LIVE_DEPLOYMENT = os.environ.get('LIVE_DEPLOYMENT', 'FALSE')
INSTANCE_NAME = os.environ.get('INSTANCE_NAME', 'Development')

# Local web server configuration items
DEBUG = bool(os.environ.get('DEBUG', False))
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get("PORT", 5000))

# Define the application directory
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

# Feature Flag Config
RAISE_ERROR_ON_MISSING_FEATURES = True

FEATURE_FLAGS = {
    'SuppressPrimaryRoleSearchLink': bool(os.environ.get('FT_SUPPRESSPRIMARYROLESEARCHLINK', False)),
}