# authentication for the mindriver api

import uuid
import hashlib
import flask
from login.api.sqlutils import sqlselect_one_user


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
        user = sqlselect_one_user(username)
    except IndexError:
        # user authentication failed
        return 403
    if not password_authenitication(password, user['password']):
        # password authentication failed
        return 403
    flask.session['username'] = username
    return 0