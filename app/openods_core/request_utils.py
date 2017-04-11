import uuid
from flask import g


# Utility method to get source_ip from a request - first checks headers for forwarded IP, then uses remote_addr if not
def get_source_ip(my_request):
    try:
        # First check for an X-Forwarded-For header provided by a proxy / router e.g. on Heroku
        source_ip = my_request.headers['X-Forwarded-For']
    except KeyError as e:
        try:
            # First check for an X-Forwarded-For header provided by a proxy / router e.g. on Heroku
            source_ip = my_request.headers['X-Client-IP']
        except KeyError as e:
            # If that header is not present, attempt to get the Source IP address from the request itself
            source_ip = my_request.remote_addr

    g.source_ip = source_ip

    return source_ip


# Utility method to get the request_id from the X-Request-Id header, and if not present generate one
def get_request_id(my_request):
    try:
        request_id = my_request.headers['X-Request-Id']
    except KeyError as e:
        request_id = str(uuid.uuid4())

    g.request_id = request_id

    return request_id
