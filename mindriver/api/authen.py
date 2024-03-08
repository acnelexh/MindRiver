# authentication for the mindriver api
import uuid
import hashlib
from datetime import datetime, timedelta
import mindriver
import sqlite3
import flask
from mindriver.api.sqlutils import sql_get_user, sql_add_user, sql_add_tmpid, sql_get_username_expiredate
from mindriver.api.utils import save_file
from flask_mail import Mail, Message

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
    dob = flask.request.form['dob']
    gender = flask.request.form['gender']
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
    password = password_hash(password)
    filename = save_file()
    try:
        sql_add_user(username, first_name, last_name, email, filename, password, dob, gender, cur)
    except sqlite3.IntegrityError:
        # user already exists
        flask.abort(409)
    flask.session['username'] = username

def user_recover(cur):
    """Help recover user."""
    username = flask.request.form['username']
    email = flask.request.form['email']
    if len(username) == 0 or len(email) == 0:
        # missing input
        flask.abort(400)
    try:
        user = sql_get_user(username, cur)
    except IndexError:
        # user authentication failed
        flask.abort(403)
    print("account found")
    if email != user['email']:
        # email authentication failed
        flask.abort(403)
    print("email found")
    # Generate a temporary link
    temporary_link = generate_temporary_link(mindriver.app.config['APPLICATION_ROOT'], username)
    print(f"temporary link generated: {temporary_link}")
    # Send recovery email
    send_recovery_email(email, temporary_link)

def generate_temporary_link(base_url, username):
    """Help generate temporary link."""
    # Generate a unique identifier
    unique_id = uuid.uuid4().hex
    # Append the unique identifier to the base URL
    temporary_link = f"{base_url}/accounts/reset_password/{unique_id}"
    # Save the unique identifier to the database
    expire_date = datetime.utcnow() + timedelta(hours=1)
    sql_add_tmpid(unique_id, username, expire_date.strftime('%Y-%m-%d %H:%M:%S.%f'))
    return temporary_link

def send_recovery_email(email, temporary_link):
    """Help send recovery email."""
    mail = Mail(app=flask.current_app)
    msg = Message(
        "Mindriver Account Recovery",
        sender=flask.current_app.config['SERVER_MAIL_ADDR'],
        recipients=[email])
    msg.body = f"Please click the link to recover your account: {temporary_link}.\n"
    msg.body += "The link will expire in 1 hour."
    mail.send(msg)

def user_password(cur):
    """Help reset password."""
    username = flask.session['username']
    password = flask.request.form['password']
    password_confirm = flask.request.form['confirm_password']
    if len(password) == 0 or len(password_confirm) == 0:
        # missing input
        flask.abort(400)
    if password != password_confirm:
        # password confirmation failed
        flask.abort(400)
    password = password_hash(password)
    cur.execute(
        "UPDATE users SET password=? WHERE username=?",
        (password, username))

def user_edit(cur):
    """Help edit user."""
    username = flask.session['username']
    first_name = flask.request.form['firstname']
    last_name = flask.request.form['lastname']
    filename = flask.request.files["file"].filename
    dob = flask.request['dob']
    gender = flask.request['gender']
    if len(first_name) == 0 or len(last_name) == 0 or len(filename) == 0:
        # missing input
        flask.abort(400)
    
