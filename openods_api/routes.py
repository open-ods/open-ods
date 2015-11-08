import logging
import status
import dicttoxml
from flask import jsonify, Response, request
from flask.ext.autodoc import Autodoc

from openods_api import app, config
import openods_api.cache as ocache
from openods_api.database import db, schema_check
from openods_api.auth import requires_auth

log = logging.getLogger('openods')

auto = Autodoc(app)

schema_check.check_schema_version()


@app.route('/')
def documentation():
    """

    Returns API documentation as HTML
    """
    return auto.html()


@auto.doc()
@app.route("/organisations", methods=['GET'])
@requires_auth
@ocache.cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
def get_organisations():

    """

    Returns a list of ODS organisations

    Params:
    - offset=x (Offset start of results [0])
    - limit=y (Limit number of results [1000])
    - recordclass=HSCOrg/HSCSite/both (filter results by recordclass [both])
    - primaryRoleCode=xxxx (filter results to only those with a specific primaryRole)
    """

    log.debug(str.format("Cache Key: {0}", ocache.generate_cache_key()))
    offset = request.args.get('offset') if request.args.get('offset') else 0
    limit = request.args.get('limit') if request.args.get('limit') else 1000
    record_class = request.args.get('recordclass') if request.args.get('recordclass') else 'both'
    primary_role_code = request.args.get('primaryRoleCode' if request.args.get('primaryRoleCode') else None)
    log.debug(offset)
    log.debug(limit)
    log.debug(record_class)
    log.debug(primary_role_code)
    data = db.get_org_list(offset, limit, record_class, primary_role_code)

    if data:
        result = {'organisations': data}
        return jsonify(result)
    else:
        return Response("404: Not Found", status.HTTP_404_NOT_FOUND )


@auto.doc()
@app.route("/organisations/<ods_code>", methods=['GET'])
@requires_auth
@ocache.cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
def get_organisation(ods_code):

    """

    Returns a specific organisation resource

    Params:
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
            result = dicttoxml.dicttoxml(data, attr_type=False, custom_root='organisation')
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
@app.route("/organisations/search/<search_text>", methods=['GET'])
@requires_auth
@ocache.cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
def search_organisations(search_text):

    """

    Returns a list of organisations

    Params:
    - offset=x (Offset start of results by x)
    - limit=y (Retrieve y results)
    """

    log.debug(str.format("Cache Key: {0}", ocache.generate_cache_key()))
    offset = request.args.get('offset') if request.args.get('offset') else 0
    limit = request.args.get('limit') if request.args.get('limit') else 1000
    log.debug(offset)
    log.debug(limit)
    orgs = db.search_organisation(search_text)

    if orgs:
        result = {'organisations': orgs}
        return jsonify(result)

    else:
        return "Not found", status.HTTP_404_NOT_FOUND


@auto.doc()
@app.route("/roles", methods=['GET'])
@requires_auth
@ocache.cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
def get_roles():

    """

    Returns the list of available OrganisationRole types
    """

    roles_list = db.get_roles()

    result = {
        'roles': roles_list
    }

    return jsonify(result)



@auto.doc()
@app.route("/roles/<role_code>", methods=['GET'])
@requires_auth
@ocache.cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
def get_role_by_code(role_code):

    """

    Returns the list of available OrganisationRole types
    """

    result = db.get_role_by_id(role_code)

    return jsonify(result)
