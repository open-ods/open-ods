import logging
import status

from flask import jsonify
from app.openods_core import cache as ocache
from app.openods_core import db
import config as config


# Utility method to get source_ip from a request - first checks headers for forwarded IP, then uses remote_addr if not
def get_source_ip(myrequest):
    try:
        source_ip = myrequest.headers['X-Client-IP']
    except KeyError as e:
        source_ip = myrequest.remote_addr

    return source_ip


@ocache.cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
def get_root_response():

    logger = logging.getLogger(__name__)
    logger.debug("Retrieving fresh data")

    root_resource = {
        'organisations': str.format('http://{0}/organisations', config.APP_HOSTNAME),
        'role-types': str.format('http://{0}/role-types', config.APP_HOSTNAME)
    }

    return root_resource


@ocache.cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
def get_info_response():

    logger = logging.getLogger(__name__)
    logger.debug("Retrieving fresh data")

    dataset_info = db.get_dataset_info()

    return dataset_info


@ocache.cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
def get_organisations_response(request):

    logger = logging.getLogger(__name__)
    logger.debug("Retrieving fresh data")

    # Collect any query parameters that were supplied
    query = request.args.get('q') if request.args.get('q') else None

    offset = request.args.get('offset') if request.args.get('offset') else 0

    limit = request.args.get('limit') if request.args.get('limit') else 20

    record_class = request.args.get(
        'recordClass') if request.args.get('recordClass') else None

    primary_role_code = request.args.get(
        'primaryRoleCode') if request.args.get('primaryRoleCode') else None

    role_code = request.args.get(
        'roleCode') if request.args.get('roleCode') else None

    postcode = request.args.get(
        'postCode') if request.args.get('postCode') else None

    # Call the get_org_list method from the database controller, passing in parameters.
    # Method will return a tuple containing the data and the total record count for the specified filter.
    data, total_record_count = db.get_org_list(offset, limit, record_class,
                                               primary_role_code, role_code,
                                               query, postcode)

    if data:
        results = {'organisations': data}
        resp = jsonify(results)
        resp.headers['X-Total-Count'] = total_record_count
        resp.headers['Access-Control-Expose-Headers'] = 'X-Total-Count'
        return resp

    else:
        result = {'organisations': [] }
        resp = jsonify(result)
        resp.headers['X-Total-Count'] = 0
        resp.headers['Access-Control-Expose-Headers'] = 'X-Total-Count'
        return resp


# Handles the request for a single organisation resource. Takes an ODS code and returns the record from the database.
# If record exists a JSON object is returned with a 200 response.
# If record does not exist a 404 response is returned.
@ocache.cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
def get_single_organisation_response(ods_code):

    logger = logging.getLogger(__name__)
    logger.debug("Retrieving fresh data")

    data = db.get_organisation_by_odscode(ods_code)

    if data:

        try:
            del data['org_lastchanged']
        except KeyError as e:
            pass

        result = jsonify(data)
        return result

    else:
        return "Not found", status.HTTP_404_NOT_FOUND


# Handles a request for a list of role-types resources.
# Returns a 200 response with a JSON object containing a list of role-type resources
# TODO: Add logic to handle no records found (low priority as shouldn't happen
@ocache.cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
def get_role_types_response(request):

    logger = logging.getLogger(__name__)
    logger.debug("Getting fresh data")

    roles_list = db.get_role_types()

    result = {
        'role-types': roles_list
    }

    return jsonify(result)


# Handles request for a specific role-type resource taking a single Role Code as the ID
# Returns a 200 response with a JSON object for the resource
# TODO: Add logic to handle record not found scenario
@ocache.cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
def get_role_type_by_code_response(request, role_code):
    """

    Returns the list of available OrganisationRole types
    """

    logger = logging.getLogger(__name__)
    logger.debug("Getting fresh data")

    result = db.get_role_type_by_id(role_code)

    return jsonify(result)