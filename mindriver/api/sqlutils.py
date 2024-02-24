import mindriver

def sqlselect_one_user(user_url_slug):
    """Get one user."""
    connection = mindriver.model.get_db()
    cur = connection.cursor()
    user = cur.execute(
        "SELECT * FROM users WHERE username=?",
        (user_url_slug,)).fetchall()
    return user[0]