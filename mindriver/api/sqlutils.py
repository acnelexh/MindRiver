"""SQL commands."""
import mindriver

def sql_select_one_user(user_url_slug):
    """Get one user."""
    connection = mindriver.model.get_db()
    cur = connection.cursor()
    user = cur.execute(
        "SELECT * FROM users WHERE username=?",
        (user_url_slug,)).fetchall()
    return user[0]

def sql_get_user(cursor, user_url_slug):
    """
    Execute SQL command.

    Input: cursor, username
    Return: mathcing user in users table
    """
    user = cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (user_url_slug,)).fetchall()
    return user[0]

