import sqlite3 as sqlite

connection = sqlite.connect('fixtures/database.sqlite')

__all__ = [
    'get_refresh_token_for_user'
]


def get_refresh_token_for_user(user_id):
    cursor = connection.cursor()
    query = 'SELECT refresh_token FROM refresh_tokens WHERE user_id = ?'
    args = [user_id]
    cursor.execute(query, args)
    row = cursor.fetchone()

    if not row:
        return None

    refresh_token = row[0]
    return refresh_token


def update_user_refresh_token(user_id, refresh_token):
    cursor = connection.cursor()
    query = 'INSERT OR REPLACE INTO refresh_tokens (user_id,refresh_token) VALUES (?,?)'
    args = [user_id, refresh_token]
    cursor.execute(query, args)
    connection.commit()
