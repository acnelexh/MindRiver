"""Mindriver model (database) API."""
import sqlite3
import flask
import mindriver


def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name.

    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_user_db():
    """Open a new database connection.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    if 'sqlite_db' not in flask.g:
        db_filename = mindriver.app.config['DATABASE_FILENAME']
        flask.g.sqlite_db = sqlite3.connect(str(db_filename))
        flask.g.sqlite_db.row_factory = dict_factory

        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")

    return flask.g.sqlite_db

def get_recover_db():
    """Init db only for keeping temporary link for password reset.
    Init db to be empty."""
    if 'sqlite_recover_db' not in flask.g:
        db_filename = mindriver.app.config['RECOVER_DATABASE_FILENAME']
        flask.g.sqlite_recover_db = sqlite3.connect(str(db_filename))
        flask.g.sqlite_recover_db.row_factory = dict_factory
        flask.g.sqlite_recover_db.execute("PRAGMA foreign_keys = ON")
        cur = flask.g.sqlite_recover_db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS recover (
                    tmpid TEXT PRIMARY KEY,
                    username TEXT NOT NULL,
                    expiredate TEXT NOT NULL
                    );""")
        flask.g.sqlite_recover_db.commit()

    return flask.g.sqlite_recover_db

@mindriver.app.teardown_appcontext
def close_db(error):
    """Close the database at the end of a request.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    assert error or not error  # Needed to avoid superfluous style error
    sqlite_db = flask.g.pop('sqlite_db', None)
    if sqlite_db is not None:
        sqlite_db.commit()
        sqlite_db.close()
    sqlite_recover_db = flask.g.pop('sqlite_recover_db', None)
    if sqlite_recover_db is not None:
        sqlite_recover_db.commit()
        sqlite_recover_db.close()
    
