# authentication for the mindriver api
import uuid
import hashlib
import sqlite3
import flask
from mindriver.api.sqlutils import sql_get_user, sql_add_user
from mindriver.api.utils import save_file

def password_authenitication(password_input, password_db):
    """Help authenticate password."""
    component = password_db.split('$')
    salt = component[1]
    input_hash = password_hash(password_input, salt)
    return input_hash == password_db


def password_hash(password, salt=uuid.uuid4().hex):
    """Help hash password."""
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password])
    return password_db_string

# operation for accounts======================================
def user_authentication():
    """Authenticate user by seesion or by username:password."""
    if "username" in flask.session:
        return 0
    if flask.request.authorization is None:
        # check for Basic Authentication
        return 403
    username = flask.request.authorization['username']
    password = flask.request.authorization['password']
    if len(username) == 0 or len(password) == 0:
        return 400
    try:
        user = sql_get_user(username)
    except IndexError:
        # user authentication failed
        return 403
    if not password_authenitication(password, user['password']):
        # password authentication failed
        return 403
    flask.session['username'] = username
    return 0

def user_login(cur):
    """Help login user."""
    username = flask.request.form['username']
    password = flask.request.form['password']
    if len(username) == 0 or len(password) == 0:
        flask.abort(400)
    try:
        user = sql_get_user(username, cur)
    except IndexError:
        # user authentication failed
        print("user authentication failed")
        flask.abort(403)
    print("user authentication passed")
    if not password_authenitication(password, user['password']):
        # password authentication failed
        flask.abort(403)
    flask.session['username'] = username

def user_create(cur):
    """Help create user."""
    first_name = flask.request.form['first_name']
    last_name = flask.request.form['last_name']
    username = flask.request.form['username']
    email = flask.request.form['email']
    password = flask.request.form['password']
    password_confirm = flask.request.form['confirm_password']
    filename = flask.request.files["file"].filename
    if len(first_name) == 0 or len(last_name) == 0 or len(username) == 0 or\
        len(email) == 0 or len(password) == 0 or len(password_confirm) == 0 or\
        len(filename) == 0:
        # missing input
        flask.abort(400)
    if password != password_confirm:
        # password confirmation failed
        flask.abort(400)
    try:
        sql_get_user(username, cur)
        flask.abort(409)
    except IndexError:
        pass
    print("create user")
    password = password_hash(password)
    filename = save_file()
    try:
        sql_add_user(username, first_name, last_name, email, filename, password, cur)
    except sqlite3.IntegrityError:
        # user already exists
        flask.abort(409)
    flask.session['username'] = username
