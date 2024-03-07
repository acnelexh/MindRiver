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

def sql_add_user(username, firstname, lastname, email, filename, password, cursor=None):
    """
    Execute SQL command.

    Input: cursor, username, firstname, lastname, email, filename, password
    Return: None
    """
    if cursor is None:
        connection = mindriver.model.get_user_db()
        cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users(username, firstname, lastname, email, filename, password) VALUES(?, ?, ?, ?, ?, ?)",
        (username, firstname, lastname, email, filename, password))

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


