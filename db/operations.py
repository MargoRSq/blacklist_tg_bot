import psycopg2

from psycopg2.extras import DictCursor
from utils.config import DATABASE_URL

from sqlalchemy import select, insert, delete


from db.schemas import Blacklist, Users
from db.db import engine, Base, metadata_obj, session

conn = 1

# blacklist_table operations

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
		where(Blacklist.id == user)
	)
	with engine.connect() as conn:
		conn.execute(delete_blacklist)
	return True


# users_table operations

def check_in_users(user):
	q = session.query(Users).filter(Users.id == user)
	return session.query(q.exists()).scalar()


def get_user_role(user):
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
