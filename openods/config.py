import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://dev:dev@localhost:5432/ods')
CACHE_TIMEOUT = int(os.environ.get('CACHE_TIMEOUT', '10'))
APP_HOSTNAME = os.environ.get('APP_HOSTNAME', 'localhost')

print(str.format("Database URL: {0}", DATABASE_URL))
print(str.format("Cache Timeout: {0}", CACHE_TIMEOUT))
print(str.format("App Hostname:: {0}", APP_HOSTNAME))