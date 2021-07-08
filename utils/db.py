import psycopg2

from telegram import Update
from telegram.ext import CallbackContext
from psycopg2.extras import DictCursor
from utils.config import DB_NAME, DB_PASSWORD, DB_USER


conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASSWORD, host='localhost')


def create_db(conn):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        create_roles = "CREATE TYPE roles AS ENUM ('superadmin', 'admin', 'user');"
        create_admins = "CREATE TABLE users(id bigint PRIMARY KEY, role roles);"

        create_blacklist = "CREATE TABLE blacklist(id bigint PRIMARY KEY, url VARCHAR(100), added_by roles);"
        # cursor.execute(create_roles)
        cursor.execute(create_blacklist)
        conn.commit()


def insert_user(conn, user, role, url):
    if not check_in_users(conn, user):
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            insert = "INSERT INTO users(id, role, url) VALUES (%s, %s, %s);"

            cursor.execute(insert, [user, role, url])
            conn.commit()
        return True
    else:
        return False


def remove_user(conn, user):
    if check_in_users(conn, user):
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            insert = "DELETE FROM users WHERE id = %s;"

            cursor.execute(insert, [user])
            conn.commit()
        return True
    else:
        return False


def check_in_blacklist(conn, user):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        select = "SELECT (id, url, added_by) FROM blacklist WHERE id = %s;"
        cursor.execute(select, [user])
        results = cursor.fetchall()

        if results:
            items = ['id', 'role', 'added_by']

            row = results[0]
            row_values = tuple(row)[0][1:-1].split(',')
            row_d = {items[i]: row_values[i]
                     for i in range(len(row_values))}

            return row_d


def check_in_users(conn, user):

    with conn.cursor(cursor_factory=DictCursor) as cursor:
        select = "SELECT (id, role, url) FROM users WHERE id = %s;"
        cursor.execute(select, [user])
        results = cursor.fetchall()

        if results:
            items = ['id', 'role', 'url']

            row = results[0]
            row_values = tuple(row)[0][1:-1].split(',')
            row_d = {items[i]: row_values[i]
                     for i in range(len(row_values))}

            return row_d

        else:
            return False


def insert_to_blacklist(conn, user, url, added_by):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        insert = "INSERT INTO blacklist(id, url, added_by) VALUES (%s, %s, %s);"
        # update = f"UPDATE blacklist SET url = '{url}' WHERE id = '{user}';"

        if not check_in_blacklist(conn, user):
            cursor.execute(insert, [user, url, added_by])
            conn.commit()

            return True
        else:
            return False


def remove_from_blacklist(conn, user):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        delete = "DELETE FROM blacklist WHERE id = %s;"

        cursor.execute(delete, [user])
        conn.commit()

        return True


def select_users_by_role(conn, role):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        select = "SELECT (id, role, url) FROM users WHERE role = %s;"

        cursor.execute(select, [role])
        results = cursor.fetchall()
        items = ['id', 'role', 'url']

        results_array = []
        for row in results:
            row_items = tuple(row)[0][1:-1].split(',')
            row_d = {items[i]: row_items[i] for i in range(len(row_items))}

            results_array.append(row_d)

        return results_array


# create_db(conn)
# insert_user(conn, 13133313, 'superadmin', 'lo.wtf')
# print(select_users_by_role(conn, 'superadmin'))


# insert_to_blacklist(conn, 12323123, 'lol.wtf', 'superadmin')
# remove_from_blacklist(conn, 12323123)
# print(check_in_blacklist(conn, 12323123))

# select_users_by_role
