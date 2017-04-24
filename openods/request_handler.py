import logging

import status
from flask import jsonify, Response

from openods import app, db
from openods import cache as ocache


@ocache.cache.cached(timeout=app.config['CACHE_TIMEOUT'], key_prefix=ocache.generate_cache_key)
def get_root_response():

    logger = logging.getLogger(__name__)
    logger.debug("Retrieving data from database")

    root_resource = {
        'organisations': str.format('{0}/organisations', app.config['APP_HOSTNAME']),
        'role-types': str.format('{0}/role-types', app.config['APP_HOSTNAME'])
    }

    return root_resource


@ocache.cache.cached(timeout=app.config['CACHE_TIMEOUT'], key_prefix=ocache.generate_cache_key)
def get_info_response():

    logger = logging.getLogger(__name__)
    logger.debug("Retrieving data from database")

    dataset_info = db.get_dataset_info()

    return dataset_info


@ocache.cache.cached(timeout=app.config['CACHE_TIMEOUT'], key_prefix=ocache.generate_cache_key)
def get_organisations_response(request):

    logger = logging.getLogger(__name__)
    logger.debug("Retrieving data from database")

    # Collect any query parameters that were supplied
    query = request.args.get('q') if request.args.get('q') else None

    offset = request.args.get('offset') if request.args.get('offset') else 0

    limit = request.args.get('limit') if request.args.get('limit') else 20

    record_class = request.args.get('recordClass') if request.args.get('recordClass') else None

    if request.args.get('primaryRoleCode'):
        primary_role_codes = request.args.get('primaryRoleCode')

        # Convert the list of comma separated role codes into a list
        temp_primary_role_code_list = primary_role_codes.split(',')

        # Convert all role codes in the list to upper case
        primary_role_code_list = [role_code.upper() for role_code in temp_primary_role_code_list]
    else:
        primary_role_code_list = None

    if request.args.get('roleCode'):
        role_codes = request.args.get('roleCode')

        # Convert the list of comma separated role codes into a list
        temp_role_code_list = role_codes.split(',')

        # Convert all role codes to upper case
        role_code_list = [role_code.upper() for role_code in temp_role_code_list]
    else:
        role_code_list = None

    postcode = request.args.get('postCode') if request.args.get('postCode') else None

    active = request.args.get('active') if request.args.get('active') else None

    last_updated_since = request.args.get('lastUpdatedSince') if request.args.get('lastUpdatedSince') else None

    # Call the get_org_list method from the database controller, passing in parameters.
    # Method will return a tuple containing the data and the total record count for the specified filter.
    data, total_record_count = db.get_org_list(offset, limit, record_class,
                                               primary_role_code_list, role_code_list,
                                               query, postcode, active, last_updated_since)

    if data:
        results = {'organisations': data}
        resp = jsonify(results)
        resp.headers['X-Total-Count'] = total_record_count
        resp.headers['Access-Control-Expose-Headers'] = 'X-Total-Count'
        return resp

    else:
        result = {'organisations': []}
        resp = jsonify(result)
        resp.headers['X-Total-Count'] = 0
        resp.headers['Access-Control-Expose-Headers'] = 'X-Total-Count'
        return resp


# Handles the request for a single organisation resource. Takes an ODS code and returns the record from the database.
# If record exists a JSON object is returned with a 200 response.
# If record does not exist a 404 response is returned.
@ocache.cache.cached(timeout=app.config['CACHE_TIMEOUT'], key_prefix=ocache.generate_cache_key)
def get_single_organisation_response(ods_code):

    logger = logging.getLogger(__name__)
    logger.debug("Retrieving data from database")

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
@ocache.cache.cached(timeout=app.config['CACHE_TIMEOUT'], key_prefix=ocache.generate_cache_key)
def get_role_types_response(request):

    logger = logging.getLogger(__name__)
    logger.debug("Retrieving data from database")

    roles_list = db.get_role_types()

    result = {
        'role-types': roles_list
    }

    return jsonify(result)


# Handles request for a specific role-type resource taking a single Role Code as the ID
# Returns a 200 response with a JSON object for the resource
# TODO: Add logic to handle record not found scenario
@ocache.cache.cached(timeout=app.config['CACHE_TIMEOUT'], key_prefix=ocache.generate_cache_key)
def get_role_type_by_code_response(request, role_code):
    """

    Returns the list of available OrganisationRole types
    """

    logger = logging.getLogger(__name__)
    logger.debug("Retrieving data from database")

    result = db.get_role_type_by_id(role_code)

    return jsonify(result)