import sqlite3 as sqlite

from tornado.options import options

__all__ = [
    'get_refresh_token_for_user',
    'update_user_refresh_token',
    'delete_user_refresh_token'
]

connection = None


def get_connection():
    """
    Lazy establish a connection.
    """
    global connection

    if not connection:
        connection = sqlite.connect(options.database_path)

    return connection


def get_refresh_token_for_user(account_uuid):
    connection = get_connection()
    cursor = connection.cursor()
    query = 'SELECT refresh_token FROM refresh_tokens WHERE account_uuid = ?'
    args = [account_uuid]
    cursor.execute(query, args)
    row = cursor.fetchone()

    if not row:
        return None

    refresh_token = row[0]
    return refresh_token


def update_user_refresh_token(account_uuid, refresh_token):
    connection = get_connection()
    cursor = connection.cursor()
    query = ('INSERT OR REPLACE INTO refresh_tokens (account_uuid,refresh_token) '
             'VALUES (?,?)')
    args = [account_uuid, refresh_token]
    cursor.execute(query, args)
    connection.commit()


def delete_user_refresh_token(account_uuid):
    connection = get_connection()
    cursor = connection.cursor()
    query = 'DELETE FROM refresh_tokens WHERE account_uuid = ?'
    args = [account_uuid]
    cursor.execute(query, args)
    connection.commit()
