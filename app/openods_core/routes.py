import logging

import status
from flask import jsonify, request
from flask_autodoc import Autodoc

import config as config
from app import app
from app.openods_core import cache as ocache
from app.openods_core import sample_data
from app.openods_core import db, schema_check
from app.openods_core import request_hander

auto = Autodoc(app)

schema_check.check_schema_version()


# Utility method to get source_ip from a request - first checks headers for forwarded IP, then uses remote_addr if not
def get_source_ip(myrequest):
    try:
        source_ip = myrequest.headers['X-Client-IP']
    except KeyError as e:
        source_ip = myrequest.remote_addr

    return source_ip


@app.route('/apidoc')
def apidoc():
    """

    Returns API documentation as HTML
    """
    return auto.html()


@auto.doc()
@app.route(config.API_URL, methods=['GET'])
def get_root():

    logger = logging.getLogger(__name__)

    logger.info("Method={method} Resource={resource} SourceAddress={source_ip} TargetURL={url}".format(
                source_ip=get_source_ip(request), resource=request.path, url=request.url, method=request.method)
                )

    root_resource = request_hander.get_root_response()

    return jsonify(root_resource)


@auto.doc()
@app.route(config.API_URL+"/info", methods=['GET'])
def get_info():

    logger = logging.getLogger(__name__)
    logger.info("Method={method} Resource={resource} SourceAddress={source_ip} TargetURL={url}".format(
                source_ip=get_source_ip(request), resource=request.path, url=request.url, method=request.method)
                )

    dataset_info = request_hander.get_info_response()

    return jsonify(dataset_info)


@auto.doc()
@app.route(config.API_URL+"/organisations", methods=['GET'])
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
    - postCode=AB1 2CD (filter organisations with match on the postcode provided)
    - active=True/False (filter organisations with the specified active status)
    """

    logger = logging.getLogger(__name__)

    logger.info("Method={method} Resource={resource} "
                "SourceAddress={source_ip} TargetURL={url}".format(
                    source_ip=get_source_ip(request), resource=request.path, url=request.url, method=request.method)
                )

    resp = request_hander.get_organisations_response(request)

    return resp


@auto.doc()
@app.route(config.API_URL+"/organisations/<ods_code>", methods=['GET'])
def get_organisation(ods_code):
    """
    Returns a specific organisation resource
    """

    logger = logging.getLogger(__name__)

    logger.info("Method={method} Resource={resource} ResourceID={resource_id} SourceAddress={source_ip} "
                "TargetURL={url}".format(
                    source_ip=get_source_ip(request), resource=request.path, resource_id=ods_code,
                    url=request.url, method=request.method)
                )

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


@auto.doc()
@app.route(config.API_URL+"/role-types", methods=['GET'])
def route_role_types():
    """

    Returns the list of available OrganisationRole types
    """

    logger = logging.getLogger(__name__)
    logger.info("Method={method} Resource={resource} SourceAddress={source_ip} TargetURL={url}".format(
        source_ip=get_source_ip(request), resource=request.path, url=request.url, method=request.method))

    result = request_hander.get_role_types_response(request)

    return result


@auto.doc()
@app.route(config.API_URL+"/role-types/<role_code>", methods=['GET'])
def route_role_type_by_code(role_code):
    """
    Returns the list of available OrganisationRole types
    """

    logger = logging.getLogger(__name__)
    logger.info("Method={method} Resource={resource} ResourceID={resource_id} SourceAddress={source_ip} "
             "TargetURL={url}".format(
              source_ip=get_source_ip(request), resource=request.path, resource_id=role_code,
              url=request.url, method=request.method)
             )

    result = request_hander.get_role_type_by_code_response(request, role_code)

    return result


@app.route(config.API_URL+"/organisations/<ods_code>/endpoints", methods=['GET'])
@ocache.cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
def organisation_endpoints(ods_code):
    """
    FAKE ENDPOINT

    Returns a list of endpoints for a specific Organisation.
    """

    return jsonify(sample_data.endpoint_data)
