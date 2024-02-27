import flask
import arrow
import mindriver

@mindriver.app.route('/')
def route_index_get():
    """Route for index page."""
    # PASS
    context = {}
    return flask.render_template("index.html", **context)

@mindriver.app.route('/accounts/login/')
def route_login_get():
    """Route for login page."""
    # PASS
    context = {}
    return flask.render_template("login.html", **context)

@mindriver.app.route('/accounts/register/')
def route_register_get():
    """Route for register page."""
    # PASS
    context = {}
    return flask.render_template("register.html", **context)


