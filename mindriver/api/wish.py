# wish editing and viewing api

import mindriver
import flask
import sqlite3
from mindriver.api.sqlutils import sql_add_wish, sql_edit_wish, sql_delete_wish, sql_get_wish

def create_wish(new_wish):
    """Create a new wish."""
    connection = mindriver.model.get_db()
    cur = connection.cursor()
    try:
        sql_add_wish(new_wish, cur)
    except sqlite3.IntegrityError:
        # wish already exists
        flask.abort(409)

def edit_wish(wish_id, new_wish):
    """Edit a wish."""
    connection = mindriver.model.get_db()
    cur = connection.cursor()
    try:
        sql_edit_wish(wish_id, new_wish, cur)
    except sqlite3.IntegrityError:
        # wish already exists
        flask.abort(409)

def delete_wish(wish_id):
    """Delete a wish."""
    connection = mindriver.model.get_db()
    cur = connection.cursor()
    try:
        sql_delete_wish(wish_id, cur)
    except sqlite3.IntegrityError:
        # wish already exists
        flask.abort(409)

def view_wish(wish_id):
    """View a wish."""
    connection = mindriver.model.get_db()
    cur = connection.cursor()
    try:
        wish = sql_get_wish(wish_id, cur)
    except IndexError:
        # wish not found
        flask.abort(404)
    return wish



