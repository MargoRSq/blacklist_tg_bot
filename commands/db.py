from telegram import Update
from telegram.ext import CallbackContext

from commands.utils import get_message_text_array, form_permission, superadmin
from db.operations import insert_user

from psycopg2.errors import DuplicateObject


def create_db(update: Update, context: CallbackContext):
	update_dict = update.to_dict()
	message = update_dict['message']

	text_array = get_message_text_array(message)

	if len(text_array) > 1:
		superadmin_id = text_array[1]
		if len(text_array) > 2:
			superadmin_url = text_array[2]

			try:
				with conn.cursor() as cursor:
					create_roles = "CREATE TYPE roles AS ENUM ('superadmin', 'admin', 'user');"
					create_users = "CREATE TABLE users(id bigint PRIMARY KEY, role roles, url VARCHAR(100));"
					create_blacklist = "CREATE TABLE blacklist(id bigint PRIMARY KEY, url VARCHAR(100), added_by roles);"

					create_array = [create_roles,
									create_users, create_blacklist]

					for create in create_array:
						cursor.execute(create)
					conn.commit()

				insert_user(superadmin_id, superadmin, superadmin_url)

			except DuplicateObject:
				update.message.reply_text('База данных уже создана!')
