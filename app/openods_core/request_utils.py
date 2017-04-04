import uuid
from flask import g


# Utility method to get source_ip from a request - first checks headers for forwarded IP, then uses remote_addr if not
def get_source_ip(my_request):
    try:
        source_ip = my_request.headers['X-Client-IP']
    except KeyError as e:
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
