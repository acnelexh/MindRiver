"""SQL commands."""
import mindriver

def sql_get_user(user_url_slug, cursor=None):
    """
    Execute SQL command.

    Input: cursor, username
    Return: mathcing user in users table
    """
    if cursor is None:
        connection = mindriver.model.get_db()
        cursor = connection.cursor()
    user = cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (user_url_slug,)).fetchall()
    return user[0]

