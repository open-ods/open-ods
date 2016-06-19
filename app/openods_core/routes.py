import logging
from flask_autodoc import Autodoc

import config
import dicttoxml
import status
from app import app
from app.openods_core import cache as ocache
from app.openods_core import sample_data
from app.openods_core.database import db, schema_check
from flask import jsonify, Response, request, render_template, json

log = logging.getLogger('openods')

auto = Autodoc(app)

schema_check.check_schema_version()


@app.route('/apidoc')
def apidoc():
    """

    Returns API documentation as HTML
    """
    return auto.html()


@auto.doc()
@app.route("/api", methods=['GET'])
@ocache.cache.cached(timeout=3600, key_prefix=ocache.generate_cache_key)
def get_root():
    root_resource = {
        'organisations': str.format('http://{0}/organisations', config.APP_HOSTNAME),
        'role-types': str.format('http://{0}/role-types', config.APP_HOSTNAME)
    }
    return jsonify(root_resource)


@auto.doc()
@app.route("/api/info", methods=['GET'])
@ocache.cache.cached(timeout=3600, key_prefix=ocache.generate_cache_key)
def get_info():
    dataset_info = db.get_dataset_info()
    return jsonify(dataset_info)



@auto.doc()
@app.route("/api/organisations", methods=['GET'])
@ocache.cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
def get_organisations():
    """

    Returns a list of ODS organisations

    Query Parameters:
    - q=xxx (Filter results by names containing q)
    - offset=x (Offset start of results [0])
    - limit=y (Limit number of results [20])
    - recordClass=HSCOrg/HSCSite (filter results by a specific recordclass)
    - primaryRoleCode=xxxx (filter results to only those with a specific primaryRole)
    - roleCode=xxxx (filter result to only those with a specific role)
    """

    log.debug(str.format("Cache Key: {0}", ocache.generate_cache_key()))

    # Collect any query parameters that were supplied
    query = request.args.get('q') if request.args.get('q') else None

    offset = request.args.get('offset') if request.args.get('offset') else 0

    limit = request.args.get('limit') if request.args.get('limit') else 20

    record_class = request.args.get(
        'recordClass') if request.args.get('recordClass') else None

    primary_role_code = request.args.get(
        'primaryRoleCode' if request.args.get('primaryRoleCode') else None)

    role_code = request.args.get(
        'roleCode' if request.args.get('roleCode') else None)

    log.debug("Offset: %s Limit: %s RecordClass: %s PrimaryRoleCode: %s RoleCode: %s Query: %s",
              offset, limit, record_class,primary_role_code,role_code,query)

    # Call the get_org_list method from the database controller, passing in parameters.
    # Method will return a tuple containing the data and the total record count for the specified filter.
    data, total_record_count = db.get_org_list(offset, limit, record_class,
                                  primary_role_code, role_code, query)

    if data:
        result = {'organisations': data}
        resp = Response(json.dumps(result), status=200, mimetype='application/json')
        resp.headers['X-Total-Count'] = total_record_count
        resp.headers['Access-Control-Expose-Headers'] = 'X-Total-Count'

        return resp
    else:
        result = {'organisations': [] }
        resp = Response(json.dumps(result), status=200, mimetype='application/json')
        resp.headers['X-Total-Count'] = total_record_count
        resp.headers['Access-Control-Expose-Headers'] = 'X-Total-Count'
        return resp


@auto.doc()
@app.route("/api/organisations/<ods_code>", methods=['GET'])
@ocache.cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
def get_organisation(ods_code):
    """

    Returns a specific organisation resource

    Query Parameters:
    - format=xml/json (Return the data in specified format - defaults to json)
    """

    format_type = request.args.get('format')
    log.debug(format_type)

    data = db.get_organisation_by_odscode(ods_code)

    if data:

        try:
            del data['org_lastchanged']

        except Exception as e:
            pass

        if format_type == 'xml':
            log.debug("Returning xml")
            result = dicttoxml.dicttoxml(
                data, attr_type=False, custom_root='organisation')
            # log.debug(result)
            return Response(result, mimetype='text/xml')

        elif format_type == 'json':
            log.debug("Returning json")
            result = jsonify(data)
            # log.debug(result)
            return result

        else:
            log.debug("Returning json")
            result = jsonify(data)
            # log.debug(result)
            return result

    else:
        return "Not found", status.HTTP_404_NOT_FOUND


@auto.doc()
@app.route("/api/role-types", methods=['GET'])
@ocache.cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
def route_role_types():
    """

    Returns the list of available OrganisationRole types
    """

    roles_list = db.get_role_types()

    result = {
        'role-types': roles_list
    }

    return jsonify(result)


@auto.doc()
@app.route("/api/role-types/<role_code>", methods=['GET'])
@ocache.cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
def route_role_type_by_code(role_code):
    """

    Returns the list of available OrganisationRole types
    """

    result = db.get_role_type_by_id(role_code)

    return jsonify(result)


@app.route("/api/organisations/<ods_code>/endpoints", methods=['GET'])
@ocache.cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
def organisation_endpoints(ods_code):
    """
    FAKE ENDPOINT

    Returns a list of endpoints for a specific Organisation.
    """

    return jsonify(sample_data.endpoint_data)
