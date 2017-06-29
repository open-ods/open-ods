import uuid
from flask import g


# Utility method to get source_ip from a request - first checks headers for forwarded IP, then uses remote_addr if not
def get_source_ip(my_request):
    try:
        # First check for an X-Forwarded-For header provided by a proxy / router e.g. on Heroku
        source_ip = my_request.headers['X-Forwarded-For']
    except KeyError:
        try:
            # First check for an X-Forwarded-For header provided by a proxy / router e.g. on Heroku
            source_ip = my_request.headers['X-Client-IP']
        except KeyError:
            # If that header is not present, attempt to get the Source IP address from the request itself
            source_ip = my_request.remote_addr

    g.source_ip = source_ip

    return source_ip


# Utility method to get the request_id from the X-Request-Id header, and if not present generate one
def get_request_id(my_request):
    try:
        request_id = my_request.headers['X-Request-Id']
    except KeyError:
        request_id = str(uuid.uuid4())

    g.request_id = request_id

    return request_id


# Utility method which takes a dict of request parameters and writes them out as pipe delimeted kv pairs
def dict_to_piped_kv_pairs(dict_for_conversion):
    output_string = ""
    for key, value in sorted(dict_for_conversion.items()):
        output_string += "{0}={1}|".format(key, value)
    return output_string
