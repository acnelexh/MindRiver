import flask
import mindriver
from mindriver.api.authen import user_login, user_create, user_recover, user_password
from mindriver.model import get_user_db


@mindriver.app.route('/accounts/', methods=['POST'])
def route_accounts_post():
    """Route for POST method account."""
    operation = flask.request.form['operation']
    connection = get_user_db()
    cur = connection.cursor()
    if operation == 'login':
        if 'username' in flask.session:
            print("already login")
            # already login, go to '/'
            return flask.redirect(flask.url_for('route_index_get'))
        user_login(cur)
    elif operation == 'create':
        if 'username' in flask.session:
            # already login, go to edit account
            return flask.redirect(flask.url_for('route_edit_get'))
        user_create(cur)
    elif operation == 'recover':
        if 'username' in flask.session:
            # already login, go to edit account
            return flask.redirect(flask.url_for('route_edit_get'))
        user_recover(cur)
    # elif operation == 'delete':
    #     if 'username' not in flask.session:
    #         # user not login
    #         flask.abort(403)
    #     user_delete(cur)
    #     flask.session.clear()
    # elif operation == 'edit_account':
    #     if 'username' not in flask.session:
    #         # user not login
    #         flask.abort(403)
    #     user_edit(cur)
    elif operation == 'reset_password':
        if 'username' not in flask.session:
            # user not login
            flask.abort(403)
        user_password(cur)
    else:
        print(f"Unrecognized operation: {operation}")
        flask.abort(404)
    return flask.redirect(flask.url_for('route_index_get'))
