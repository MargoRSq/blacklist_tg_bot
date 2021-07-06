import psycopg2

from psycopg2.extras import DictCursor
from config import DB_NAME, DB_PASSWORD, DB_USER

from psycopg2.errors import UniqueViolation

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
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        insert = f"INSERT INTO users(id, role, url) VALUES ({user}, '{role}', '{url}');"

        cursor.execute(insert)
        conn.commit()


def check_in_blacklist(conn, user):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        select = f"SELECT (id, url) FROM blacklist WHERE id = {user};"
        cursor.execute(select)
        results = cursor.fetchall()

        if results:
            return True
        else:
            return False


def insert_to_blacklist(conn, user, url, added_by):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        insert = f"INSERT INTO blacklist(id, url, added_by) VALUES ({user}, '{url}', '{added_by}');"
        update = f"UPDATE blacklist SET url = '{url}' WHERE id = {user};"

        try:
            cursor.execute(insert)
            conn.commit()

            return True
        except UniqueViolation:
            cursor.execute(update, (user, url))
            conn.commit()

            return False


def remove_from_blacklist(conn, user):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        delete = f"DELETE FROM blacklist WHERE id = {user};"

        if not check_in_blacklist(conn, user):
            cursor.execute(delete)
            conn.commit()

            return True


def select_users_by_role(conn, role):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        select = f"SELECT (id, role, url) FROM users WHERE role = '{role}';"

        cursor.execute(select)
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
print(check_in_blacklist(conn, 12323123))
