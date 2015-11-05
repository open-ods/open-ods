import logging
from dict2xml import dict2xml as xmlify
from flask import jsonify, Response, request
from flask.ext.autodoc import Autodoc

from openods import app, config
import openods.cache as ocache
from openods.cache import cache
from openods.database import db

log = logging.getLogger('openods')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)

auto = Autodoc(app)


@app.route('/')
@app.route('/docs')
@auto.doc()
def documentation():
    '''
    Returns API documentation as HTML
    '''
    return auto.html()


@app.route("/organisations/<ods_code>", methods=['GET'])
@auto.doc()
@cache.cached(timeout=config.CACHE_TIMEOUT)
def get_organisation(ods_code):
    '''
    Returns a specific organisation resource
    '''
    data = db.get_org(ods_code)
    if data:

        try:
            del data['org_lastchanged']

        except Exception as e:
            pass

        log.debug(jsonify(data))
        return jsonify(data)
    else:
        return "Not found", 404


@app.route("/organisations", methods=['GET'])
@auto.doc()
@cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
def get_organisations():

    '''
    Returns a list of organisations

    Params:
    - offset=x (Offset start of results by x)
    - limit=y (Retrieve y results)
    '''

    log.debug(str.format("Cache Key: {0}", ocache.generate_cache_key()))
    offset = request.args.get('offset') if request.args.get('offset') else 0
    limit = request.args.get('limit') if request.args.get('limit') else 1000
    log.debug(offset)
    log.debug(limit)
    orgs = db.get_org_list(offset, limit)
    result = {'organisations': orgs}
    return jsonify(result)


@app.route("/organisations/latest", methods=['GET'])
def get_latest_organisation():
    format_type = request.args.get('format')
    log.debug(format_type)
    data = db.get_latest_org()
    del data['org_lastchanged']

    if format_type == 'xml':
        log.debug("Returning xml")
        xml = xmlify(data, wrap="all", indent="  ")
        log.debug(xml)
        return Response(xml, mimetype='text/xml')

    elif format_type == 'json':
        log.debug("Returning json")
        result = jsonify(data)
        log.debug(result)
        return result

    else:
        log.debug("Returning json")
        result = jsonify(data)
        log.debug(result)
        return result


@app.route("/organisations/<ods_code>/document", methods=['GET'])
@auto.doc()
@cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
def get_organisation_document(ods_code):

    '''
    EXPERIMENTAL: Returns an organisation document directly from document store
    '''
    data = db.get_org_doc(ods_code)
    if data:
        try:
            del data['org_lastchanged']
        except Exception as e:
            pass
        log.debug(jsonify(data))
        return jsonify(data)
    else:
        return "Not found", 404


@app.route("/roles", methods=['GET'])
@auto.doc()
@cache.cached(timeout=config.CACHE_TIMEOUT, key_prefix=ocache.generate_cache_key)
def get_roles():

    '''
    Returns the list of available OrganisationRole types
    '''

    roles = db.get_roles()
    log.debug(roles)
    result = { 'roles': roles }
    return jsonify(result)