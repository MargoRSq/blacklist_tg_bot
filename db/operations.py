from sqlalchemy import select, insert, delete

from db.schemas import Blacklist, Users, StateSaver
from db.db import engine, session



def check_state(user):
    q = session.query(StateSaver).filter(StateSaver.id == user)
    if session.query(q.exists()).scalar():
        select_state = (
            select(StateSaver.state).
            where(StateSaver.id == user)
        )
        with engine.connect() as conn:
            result = conn.execute(select_state)
        return result.fetchone()[0].value
    else:
        return 0

def set_state(user, st):
    if not check_state(user):
        insert_state = (
            insert(StateSaver).
            values(id=user, state=st))
        with engine.connect() as conn:
            conn.execute(insert_state)
        return True
    else:
        return False

def unset_state(user):
    delete_state = (
        delete(StateSaver).
        where(StateSaver.id == user)
    )
    with engine.connect() as conn:
        conn.execute(delete_state)
    return True


def form_ids_list(roles: list):
    permissions_list = []
    for role in roles:
        permissions_list.extend(select_users_by_role(role))
    return [*permissions_list, 0]


# blacklist_table operations
def check_in_blacklist(user):
    q = session.query(Blacklist).filter(Blacklist.id == user)
    return session.query(q.exists()).scalar()


def count_blacklist():
    return session.query(Blacklist.id).count()


def insert_to_blacklist(user,
                        url,
                        added_by,
                        chat_id,
                        message_id,
                        chat_type,
                        chat_name):
    if not check_in_blacklist(user):
        insert_blacklist = (
            insert(Blacklist).
            values(id=user, url=url,
                   added_by=added_by, chat_id=chat_id,
                   message_id=message_id, chat_type=chat_type,
                   chat_name=chat_name)
        )
        with engine.connect() as conn:
            conn.execute(insert_blacklist)
        return True
    else:
        return False


def remove_from_blacklist(user):
    delete_blacklist = (
        delete(Blacklist).
        where(Blacklist.id == user)
    )
    with engine.connect() as conn:
        conn.execute(delete_blacklist)
    return True


def select_from_blacklist(to_select, user):
    select_user = (
        select(to_select).
        where(Blacklist.id == user)
    )
    with engine.connect() as conn:
        results = conn.execute(select_user)
        return results.fetchone()[0]


# users_table operations
def check_in_users(user):
    q = session.query(Users).filter(Users.id == user)
    return session.query(q.exists()).scalar()

def count_users_by_role(role):
    return session.query(Users).filter(Users.role == role).count()


def get_user_role(user):
    if user == 0:
        return 'admin'
    else:
        select_role = (
            select(Users.role).
            where(Users.id == user)
        )
        with engine.connect() as conn:
            result = conn.execute(select_role)
        return result.fetchone()[0].value


def insert_user(user, role, url):
    if not check_in_users(user):
        insert_users = (
            insert(Users).
            values(id=user, url=url, role=role)
        )
        with engine.connect() as conn:
            conn.execute(insert_users)
        return True
    else:
        return False


def select_users_by_role(role):
    select_role = (
        select(Users).
        where(Users.role == role)
    )
    with engine.connect() as conn:
        results = conn.execute(select_role)
        return results.scalars().all()


def remove_user(user):
    if check_in_users(user):
        delete_users = (
            delete(Users).
            where(Users.id == user)
        )
        with engine.connect() as conn:
            conn.execute(delete_users)
        return True
    else:
        return False
