import flask
import arrow
import login

@login.app.route('/')
def route_index_get():
    """Route for index page."""
    # PASS
    context = {}
    return flask.render_template("index.html", **context)

@login.app.route('/accounts/login/')
def route_login_get():
    """Route for login page."""
    # PASS
    context = {}
    return flask.render_template("login.html", **context)