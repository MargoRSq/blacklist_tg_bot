import psycopg2

from psycopg2.extras import DictCursor
from utils.config import DATABASE_URL

from sqlalchemy import select, insert, delete


from db.schemas import Blacklist
from db.db import engine, Base, metadata_obj, session


def check_in_blacklist(user):
    q = session.query(Blacklist).filter(Blacklist.id == user)
    return session.query(q.exists()).scalar()


def count_blacklist():
    return len(list(session.execute(
        select(Blacklist.id))))


def insert_to_blacklist(user, url, added_by, chat_id, message_id):
    if not check_in_blacklist(user):
        insert_blacklist = (
            insert(Blacklist).
            values(id=user, url=url, added_by=added_by,
                   chat_id=chat_id, message_id=message_id)
        )
        with engine.connect() as conn:
            conn.execute(insert_blacklist)
        return True
    else:
        return False


def remove_from_blacklist(user):
    delete_blacklist = (
        delete(Blacklist).
        where(Blacklist.c.id == user)
    )
    with engine.connect() as conn:
        conn.execute(delete_blacklist)
    return True


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


def insert_user(user, role, url):
    if not check_in_users(user):
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
