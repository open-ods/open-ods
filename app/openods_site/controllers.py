# Import flask dependencies
from app import app
from flask import Blueprint, render_template

# Define the blueprint: 'site', set its url prefix: app.url/
mod_site = Blueprint('site', __name__, url_prefix='/')


# Define the routes for this blueprint
@mod_site.route('', methods=['GET'])
def index():
    """

    Returns API documentation as HTML
    """
    return render_template('openods_site/index.html', instance_name=app.config['INSTANCE_NAME'], live_deployment=app.config['LIVE_DEPLOYMENT'])


@mod_site.route('try', methods=['GET'])
def tryit():
    return render_template('openods_site/tryit.html')


@mod_site.route('documentation', methods=['GET'])
def documentation():
    """

    Returns API documentation as HTML
    """
    return render_template('openods_site/documentation.html')


@mod_site.route('resources', methods=['GET'])
def resources():
    """

    Returns API documentation as HTML
    """
    return render_template('openods_site/resources.html')