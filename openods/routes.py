import logging
import os

from flasgger import Swagger
from flask import jsonify, request, g, json, redirect, url_for, send_from_directory

from openods import app
from openods import request_handler, request_utils
from openods.config_swagger import template

swagger = Swagger(app, template=template)


# HTTP error handling
@app.errorhandler(404)
def not_found(error):

    request_utils.get_request_id(request)
    request_utils.get_source_ip(request)

    logger = logging.getLogger(__name__)

    logger.info('NotFound|requestId={request_id}|statusCode={status_code}|'
                'errorDescription="{error_description}"|path="{path}"|'
                'sourceIp={source_ip}|url="{url}"|'.format(
                    request_id=g.request_id,
                    source_ip=g.source_ip,
                    path=request.path,
                    url=request.url,
                    status_code=error.code,
                    error_description=error.description)
                )

    return jsonify(
        {
            'errorCode': 404,
            'errorText': 'Not found'
        }
    ), 404


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'openods.ico', mimetype='image/vnd.microsoft.icon')


@app.route(app.config['API_PATH'] + '/v1' + '/status')
def get_status():
    return jsonify(
        {
            'status': 'OK'
        }
    )


@app.route('/')
def root():
    return redirect(url_for('get_root'))


@app.route(app.config['API_PATH'], methods=['GET'])
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

    logger.info('Request|requestId={request_id}|statusCode={status_code}|path="{path}"|'
                'sourceIp={source_ip}|url="{url}"|parameters={parameters}|'.format(
                    request_id=g.request_id,
                    source_ip=g.source_ip,
                    path=request.path,
                    url=request.url,
                    parameters=json.dumps(request.args),
                    status_code=200)
                )

    logger.debug('requestId={request_id}|headers={headers}|'.format(
        headers=json.dumps(dict(request.headers)),
        request_id=g.request_id)
    )

    root_resource = request_handler.get_root_response()

    return jsonify(root_resource)


@app.route(app.config['API_PATH'] + "/info", methods=['GET'])
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
    logger.info('logType=Request, requestId={request_id}, '
                'path="{path}", sourceIp={source_ip}, url="{url}"'.format(
                    request_id=g.request_id,
                    source_ip=g.source_ip,
                    path=request.path,
                    url=request.url,
                    )
                )

    dataset_info = request_handler.get_info_response()

    return jsonify(dataset_info)


@app.route(app.config['API_PATH'] + "/organisations", methods=['GET'])
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

    logger.info('logType=Request, requestId={request_id}, path="{path}", sourceIp={source_ip}, '
                'url="{url}", parameters={parameter_json}'.format(
                    source_ip=g.source_ip,
                    request_id=g.request_id,
                    path=request.path,
                    url=request.url,
                    parameter_json=json.dumps(request.args)
                    )
                )

    resp = request_handler.get_organisations_response(request)

    return resp


@app.route(app.config['API_PATH'] + "/organisations/<ods_code>", methods=['GET'])
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
    logger.info('logType=Request, requestId={request_id}, path="{path}", '
                'resourceId={resource_id}, sourceIp={source_ip}, url="{url}"'.format(
                    request_id=g.request_id,
                    source_ip=g.source_ip,
                    path=request.path,
                    resource_id=ods_code,
                    url=request.url,
                    )
                )

    response = request_handler.get_single_organisation_response(ods_code)

    return response


@app.route(app.config['API_PATH'] + "/role-types", methods=['GET'])
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
    logger.info('logType=Request, requestId={request_id}, '
                'path="{path}", sourceIp={source_ip}, url="{url}", parameters={parameter_json}'.format(
                    source_ip=g.source_ip,
                    request_id=g.request_id,
                    path=request.path,
                    url=request.url,
                    parameter_json=json.dumps(request.args),
                    )
                )

    result = request_handler.get_role_types_response(request)

    return result


@app.route(app.config['API_PATH'] + "/role-types/<role_code>", methods=['GET'])
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
    logger.info('logType=Request, requestId={request_id}, path="{path}", '
                'resourceId={resource_id}, sourceIp={source_ip}, url="{url}"'.format(
                    source_ip=g.source_ip,
                    request_id=g.request_id,
                    resource_id=role_code,
                    path=request.path,
                    url=request.url,
                    )
                )

    result = request_handler.get_role_type_by_code_response(request, role_code)

    return result
