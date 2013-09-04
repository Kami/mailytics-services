import sqlite3 as sqlite

from tornado.options import options

connection = sqlite.connect(options.database_path)

__all__ = [
    'get_refresh_token_for_user',
    'update_user_refresh_token',
    'delete_user_refresh_token'
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
    query = ('INSERT OR REPLACE INTO refresh_tokens (user_id,refresh_token) '
             'VALUES (?,?)')
    args = [user_id, refresh_token]
    cursor.execute(query, args)
    connection.commit()


def delete_user_refresh_token(user_id):
    cursor = connection.cursor()
    query = 'DELETE FROM refresh_tokens WHERE user_id = ?'
    args = [user_id]
    cursor.execute(query, args)
    connection.commit()


def get_access_token_for_user(user_id, expires_threshold):
    cursor = connection.cursor()
    query = ('SELECT access_token FROM access_tokens_cache WHERE user_id = ? '
             'AND expires_at <= ?')

    args = [user_id, expires_threshold]
    cursor.execute(query, args)
    row = cursor.fetchone()

    if not row:
        return None

    access_token = row[0]
    return access_token


def update_user_access_token(user_id, access_token, expires_at):
    cursor = connection.cursor()
    query = ('INSERT OR REPLACE INTO access_tokens_cache(user_id,access_token,'
             'expires_at) VALUES (?,?,?)')
    args = [user_id, access_token, expires_at]
    cursor.execute(query, args)
    connection.commit()
