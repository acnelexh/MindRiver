import flask
import arrow
import mindriver
from mindriver.model import get_user_db
from datetime import datetime
from mindriver.api.sqlutils import sql_get_username_expiredate

@mindriver.app.route('/')
def route_index_get():
    """Route for index page."""
    # PASS
    try:
        login_user = flask.session['username']
    except KeyError:
        return flask.redirect(flask.url_for('route_login_get'))
    context = {}
    context['user'] = login_user
    connection = get_user_db()
    cur = connection.cursor()
    return flask.render_template("index.html", **context)

@mindriver.app.route('/accounts/login/')
def route_login_get():
    """Route for login page."""
    # PASS
    context = {}
    return flask.render_template("login.html", **context)

@mindriver.app.route('/accounts/logout/')
def route_logout_get():
    """Route for logout page."""
    # PASS
    flask.session.clear()
    return flask.redirect(flask.url_for('route_index_get'))

@mindriver.app.route('/accounts/create/')
def route_register_get():
    """Route for register page."""
    # PASS
    context = {}
    return flask.render_template("register.html", **context)

@mindriver.app.route('/accounts/recover/')
def route_recover_get():
    """Route for recover page."""
    # PASS
    context = {}
    return flask.render_template("recover.html", **context)

@mindriver.app.route('/reset_password/<string:unique_id>')
def route_reset_password_get(unique_id):
    """Route for reset password page."""
    try:
        result = sql_get_username_expiredate(unique_id)
    except IndexError:
        # unique id not found
        flask.abort(404)
    username = result['username']
    expire_date = result['expiredate']
    if datetime.utcnow() > datetime.strptime(expire_date, '%Y-%m-%d %H:%M:%S.%f'):
        # unique id expired
        flask.abort(410)
    else:
        # unique id is valid
        flask.session['username'] = username
        return flask.render_template("reset.html")