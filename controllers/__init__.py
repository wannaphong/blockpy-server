import os

from flask import session, g, send_from_directory, request, jsonify, render_template
from flask import redirect, url_for
from flask_security.core import current_user

from main import app
from models.models import db, User, Course
from controllers.helpers import (admin_required, lti, highlight_python_code)

app.jinja_env.filters['highlight_python_code'] = highlight_python_code

@app.before_request
def load_user():
    if current_user.is_authenticated:
        g.user = current_user
        if 'lti_course' in session:
            g.course = Course.by_id(session['lti_course'])
    else:
        g.user = None

from controllers.admin import admin

import controllers.security 

from controllers.users import users
app.register_blueprint(users)

from controllers.courses import courses
app.register_blueprint(courses)

from controllers.assignments import blueprint_assignments
app.register_blueprint(blueprint_assignments)

from controllers.assignment_groups import blueprint_assignment_group
app.register_blueprint(blueprint_assignment_group)

from controllers.blockpy import blueprint_blockpy
app.register_blueprint(blueprint_blockpy)

from controllers.maze import blueprint_maze
app.register_blueprint(blueprint_maze)

from controllers.corgis import blueprint_corgis, blueprint_datasets
app.register_blueprint(blueprint_corgis)
app.register_blueprint(blueprint_datasets)

@app.route('/', methods=['GET', 'POST'])
def index():
    """ initial access page to the lti provider.  This page provides
    authorization for the user.

    :param lti: the `lti` object from `pylti`
    :return: index page for lti provider
    """
    return render_template('index.html')
    
@app.route('/about/', methods=['GET', 'POST'])
@app.route('/about', methods=['GET', 'POST'])
def about():
    """
    Information about the various projects.
    """
    return render_template('about.html')
    
@app.route('/contact/', methods=['GET', 'POST'])
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Information on how to contact the developers
    """
    return render_template('contact.html')

@app.route('/favicon.ico', methods=['GET', 'POST'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
@app.route("/site-map", methods=['GET', 'POST'])
def site_map():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        try:
            url = url_for(rule.endpoint, **options)
        except:
            url = "Unknown error"
        line = urllib.unquote("<td>{:50s}</td><td>{:20s}</td><td>{}</td>".format(rule.endpoint, methods, url))
        output.append(line)
    return "<table><tr>{}</tr></table>".format("</tr><tr>".join(sorted(output)))
