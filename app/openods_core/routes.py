import logging

import status
from flask import jsonify, request, g, json, render_template
from flasgger import Swagger

import config as config
from app import app
from app.openods_core.config_swagger import template
# from app.openods_core import cache as ocache
# from app.openods_core import sample_data
from app.openods_core import db, schema_check
from app.openods_core import request_handler, request_utils

swagger = Swagger(app, template=template)

schema_check.check_schema_version()


# HTTP error handling
@app.errorhandler(404)
def not_found(error):

    request_utils.get_request_id(request)
    request_utils.get_source_ip(request)

    logger = logging.getLogger(__name__)

    log_event = {
        'method': request.method,
        'requestId': g.request_id,
        'sourceIp': g.source_ip,
        'url': request.url,
        'statusCode': error.code,
        'errorDescription': error.description
    }

    logger.info("API_REQUEST_JSON {log_event}".format(log_event=json.dumps(log_event)))

    return render_template('404.html'), 404


@app.route(config.API_URL, methods=['GET'])
def get_root():
    """Endpoint returning information about available resources
    ---
    responses:
      200:
        description: A list of resources available through the API
    """

    logger = logging.getLogger(__name__)

    request_utils.get_request_id(request)
    request_utils.get_source_ip(request)

    logger.info("API_REQUEST method={method} requestId={request_id} path={path} "
                "sourceIp={source_ip} url={url}".format(
                    request_id=g.request_id,
                    source_ip=g.source_ip,
                    path=request.path,
                    url=request.url,
                    method=request.method)
                )

    log_event = {
        'method': request.method,
        'requestId': g.request_id,
        'sourceIp': g.source_ip,
        'path': request.path,
        'url': request.url,
        'parameters': request.args,
        'statusCode': 200
    }

    logger.info("API_REQUEST_JSON {log_event}".format(log_event=json.dumps(log_event)))

    logger.debug("requestId={request_id} headers={headers}".format(
        headers=json.dumps(dict(request.headers)),
        request_id = g.request_id)
    )

    root_resource = request_handler.get_root_response()

    return jsonify(root_resource)


@app.route(config.API_URL+"/info", methods=['GET'])
def get_info():
    """Endpoint returning information about the current ODS dataset
    ---
    responses:
      200:
        description: A JSON object representing the metadata about the ODS dataset currently in use by the API
    """
    request_utils.get_request_id(request)
    request_utils.get_source_ip(request)

    logger = logging.getLogger(__name__)
    logger.info("API_REQUEST method={method} requestId={request_id} "
                "path={resource} sourceIp={source_ip} url={url}".format(
                    request_id=g.request_id,
                    source_ip=g.source_ip,
                    resource=request.path,
                    url=request.url,
                    method=request.method
                    )
                )

    dataset_info = request_handler.get_info_response()

    return jsonify(dataset_info)


@app.route(config.API_URL+"/organisations", methods=['GET'])
def get_organisations():
    """
    Endpoint returning a list of ODS organisations
    ---
    parameters:
      - name: limit
        description: Limits number of results to specified value (hard limit of 1000 records)
        in: query
        type: integer
        required: false
      - name: offset
        description: Starts result set at specified point in the total results set
        in: query
        type: integer
        required: false
      - name: q
        description: Filters results by names which contain the specified string
        in: query
        type: string
        required: false
      - name: postCode
        description: Filters results to only those with a postcode containing the specified value
        in: query
        type: string
      - name: active
        description: true - filters results to only those with a status of 'Active'.
          false - filters results to only those with a status of 'Inactive'
        in: query
        type: boolean
      - name: roleCode
        description: Filters results to only those with one of the specified role codes assigned
        in: query
        type: array
        collectionFormat: csv
        required: false
      - name: primaryRoleCode
        description: Filters results to only those with one of the specified role codes assigned as a Primary role.
          Ignored if used alongside roleCode parameter.
        in: query
        type: array
        collectionFormat: csv
        required: false
      - name: lastUpdatedSince
        description: Filters results to only those with a lastChangeDate after the specified date.
        in: query
        type: string
        format: date
        required: false
      - name: recordClass
        description: Filters results to only those in the specified record class.
        in: query
        type: string
        enum: ['HSCSite', 'HSCOrg']
        required: false
    responses:
      200:
        description: A filtered list of organisation resources
    """

    request_utils.get_request_id(request)
    request_utils.get_source_ip(request)

    logger = logging.getLogger(__name__)

    logger.info("API_REQUEST method={method} requestId={request_id} "
                "path={path} parameters={parameter_json} sourceIp={source_ip} url={url}".format(
                    method=request.method,
                    source_ip=g.source_ip,
                    request_id=g.request_id,
                    path=request.path,
                    url=request.url,
                    parameter_json=json.dumps(request.args)
                    )
                )

    resp = request_handler.get_organisations_response(request)

    return resp


@app.route(config.API_URL+"/organisations/<ods_code>", methods=['GET'])
def get_organisation(ods_code):
    """Endpoint returns a single ODS organisation
        ---
        parameters:
          - name: ods_code
            in: path
            type: string
            required: true
        responses:
          200:
            description: A single JSON object representing an ODS organisation record
        """

    request_utils.get_request_id(request)
    request_utils.get_source_ip(request)
    logger = logging.getLogger(__name__)

    logger.info("API_REQUEST method={method} requestId={request_id} path={path} "
                "resourceId={resource_id} sourceIp={source_ip} url={url}".format(
                    method=request.method,
                    request_id=g.request_id,
                    source_ip=g.source_ip,
                    path=request.path,
                    resource_id=ods_code,
                    url=request.url,
                    )
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


@app.route(config.API_URL+"/role-types", methods=['GET'])
def route_role_types():
    """
        Endpoint returning a list of ODS role types
        ---
        responses:
          200:
            description: A list of ODS role type resources
        """

    request_utils.get_request_id(request)
    request_utils.get_source_ip(request)

    logger = logging.getLogger(__name__)
    logger.info("API_REQUEST method={method} requestId={request_id} "
                "path={path} parameters={parameter_json} sourceIp={source_ip} url={url}".format(
                    method=request.method,
                    source_ip=g.source_ip,
                    request_id=g.request_id,
                    path=request.path,
                    url=request.url,
                    parameter_json=json.dumps(request.args),
                    )
                )

    result = request_handler.get_role_types_response(request)

    return result


@app.route(config.API_URL+"/role-types/<role_code>", methods=['GET'])
def route_role_type_by_code(role_code):
    """Endpoint returns a single ODS role type
        ---
        parameters:
          - name: role_code
            in: path
            type: string
            required: true
        responses:
          200:
            description: A single JSON object representing an ODS role type record
        """
    request_utils.get_request_id(request)
    request_utils.get_source_ip(request)

    logger = logging.getLogger(__name__)
    logger.info("API_REQUEST method={method} requestId={request_id} path={path} "
                "resourceId={resource_id} sourceIp={source_ip} url={url}".format(
                    method=request.method,
                    source_ip=g.source_ip,
                    request_id=g.request_id,
                    resource_id=role_code,
                    path=request.path,
                    url=request.url,
                    )
                )

    result = request_handler.get_role_type_by_code_response(request, role_code)

    return result

#
# @app.route(config.API_URL+"/organisations/<ods_code>/endpoints", methods=['GET'])
# @ocache.cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
# def organisation_endpoints(ods_code):
#     """
#     FAKE ENDPOINT
#
#     Returns a list of endpoints for a specific Organisation.
#     """
#
#     return jsonify(sample_data.endpoint_data)
