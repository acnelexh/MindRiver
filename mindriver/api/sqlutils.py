"""SQL commands."""
import mindriver

def sql_get_user(user_url_slug, cursor=None):
    """
    Execute SQL command.

    Input: cursor, username
    Return: mathcing user in users table
    """
    if cursor is None:
        connection = mindriver.model.get_user_db()
        cursor = connection.cursor()
    user = cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (user_url_slug,)).fetchall()
    return user[0]

def sql_add_user(username, firstname, lastname, email, filename, password, dob, gender, cursor=None):
    """
    Execute SQL command.

    Input: cursor, username, firstname, lastname, email, filename, password
    Return: None
    """
    if cursor is None:
        connection = mindriver.model.get_user_db()
        cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO users (
            username, firstname, lastname, email, filename, password, dob, gender) 
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
        (username, firstname, lastname, email, filename, password, dob, gender))

def sql_add_tmpid(tmpid, username, expiry_date, cursor=None):
    """
    Execute SQL command.

    Input: tmpid, expiry_date, cursor
    Return: None
    """
    if cursor is None:
        connection = mindriver.model.get_recover_db()
        cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO recover(tmpid, username, expiredate) VALUES(?, ?, ?)",
        (tmpid, username, expiry_date))

def sql_get_username_expiredate(tmpid, cursor=None):
    """
    Execute SQL command.

    Input: tmpid, cursor
    Return: matching expire date and username in recover table
    """
    if cursor is None:
        connection = mindriver.model.get_recover_db()
        cursor = connection.cursor()
    result = cursor.execute(
        "SELECT expiredate, username FROM recover WHERE tmpid=?", (tmpid,)).fetchall()
    return result[0]


def sql_add_wish(wish, cursor=None):
    """
    Execute SQL command.

    Input: cursor, wish
    Return: None
    """
    if cursor is None:
        connection = mindriver.model.get_db()
        cursor = connection.cursor()
    wish_id = cursor.execute(
        "SELECT MAX(wish_id) FROM wishes").fetchall()[0][0] + 1
    cursor.execute(
        "INSERT INTO wishes (username, wish, wish_id) VALUES(?, ?, ?)",
        (mindriver.api.authen.get_username(), wish, wish_id))

def sql_edit_wish(wish_id, new_wish, cursor=None):
    """
    Execute SQL command.

    Input: cursor, wish_id, new_wish
    Return: None
    """
    if cursor is None:
        connection = mindriver.model.get_db()
        cursor = connection.cursor()
    cursor.execute(
        "UPDATE wishes SET wish=? WHERE wish_id=?",
        (new_wish, wish_id))
    
def sql_delete_wish(wish_id, cursor=None):
    """
    Execute SQL command.

    Input: cursor, wish_id
    Return: None
    """
    if cursor is None:
        connection = mindriver.model.get_db()
        cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM wishes WHERE wish_id=?", (wish_id,))

def sql_get_wish(wish_id, cursor=None):
    """
    Execute SQL command.

    Input: cursor, wish_id
    Return: matching wish in wishes table
    """
    if cursor is None:
        connection = mindriver.model.get_db()
        cursor = connection.cursor()
    wish = cursor.execute(
        "SELECT wish FROM wishes WHERE wish_id=?", (wish_id,)).fetchall()
    return wish[0][0]

def sql_get_user_wishes(cursor=None):
    """
    Execute SQL command.

    Input: cursor
    Return: all wishes for a user
    """
    if cursor is None:
        connection = mindriver.model.get_db()
        cursor = connection.cursor()
    wishes = cursor.execute(
        "SELECT wish_id, wish FROM wishes WHERE username=?",
        (mindriver.api.authen.get_username(),)).fetchall()
    return wishes