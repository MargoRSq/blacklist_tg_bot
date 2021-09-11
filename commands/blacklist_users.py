from telegram import Update
from telegram.ext import CallbackContext

from commands.utils import get_message_text_array, raise_invalid_id, form_permission, admin, superadmin
from utils.db import (
	check_in_blacklist,
	conn,
	insert_to_blacklist,
	remove_from_blacklist,
	count_blacklist
)

add_text = """
/add {user_id} {url} - Добавить или обновить ссылку на человека
Пример: /add 88888888 https://www.t.me...
"""
remove_text = """
/remove {user_id} - Удалить человека из базы данных
Пример: /remove 88888888
"""
check_text = """
/check {user_id} - Проверить id на наличие в блэк листах
Пример: /check 88888888
"""

added_to_blacklist_text = 'Пользователь добавлен в черный список!'
removed_from_blacklist_text = 'Пользователь удален из черного списка!'
already_in_blacklist_text = 'Пользователь уже находился в черном списке!'
not_in_blackilist_text = 'Пользователя нет в черном списке!'
in_blacklist_text = 'Пользователь в черном списке!'

no_permission = 'У вас недостаточно прав!'


def append_user_blacklist(update: Update, context: CallbackContext) -> None:

	update_dict = update.to_dict()
	message = update_dict['message']
	text_array = get_message_text_array(message)

	permissions = form_permission([admin, superadmin])
	permissions_dict = permissions['dict']
	permissions_list = permissions['list']

	superadmins = permissions_dict[superadmin]

	from_id = message['from']['id']

	if len(text_array) > 1:
		user_id = text_array[1]
		if raise_invalid_id(user_id, update):
			url = ''
			if len(text_array) > 2:
				url = text_array[2]

			if from_id in permissions_list:

				if from_id in superadmins:
					result = insert_to_blacklist(
						conn, user_id, url, superadmin)
				else:
					result = insert_to_blacklist(conn, user_id, url, admin)

				if result:
					update.message.reply_text(added_to_blacklist_text)
				else:
					update.message.reply_text(already_in_blacklist_text)

			elif from_id not in permissions_list:
				update.message.reply_text(no_permission)
	else:
		if from_id in permissions_list:
			update.message.reply_text(add_text)


def remove_user_blacklist(update: Update, context: CallbackContext) -> None:

	update_dict = update.to_dict()
	message = update_dict['message']
	text_array = get_message_text_array(message)

	permissions = form_permission([admin, superadmin])
	permissions_dict = permissions['dict']
	permissions_list = permissions['list']

	superadmins = permissions_dict[superadmin]

	from_id = message['from']['id']

	if len(text_array) > 1:
		user_id = text_array[1]
		raise_invalid_id(user_id, update)

		if from_id in permissions_list:

			is_in_blacklist = check_in_blacklist(conn, user_id)

			if is_in_blacklist:
				added_by = is_in_blacklist['added_by']

				if added_by == superadmin and from_id in superadmins:
					result = remove_from_blacklist(conn, user_id)
					if result:
						update.message.reply_text(removed_from_blacklist_text)

				elif added_by == admin and from_id in permissions_list:
					result = remove_from_blacklist(conn, user_id)
					if result:
						update.message.reply_text(
							removed_from_blacklist_text)

				elif added_by == superadmin and from_id not in superadmins:
					update.message.reply_text(no_permission)
			else:
				update.message.reply_text(not_in_blackilist_text)

	else:
		if from_id in permissions_list:
			update.message.reply_text(add_text)


def check_user_blacklist(update: Update, context: CallbackContext) -> None:

	update_dict = update.to_dict()
	message = update_dict['message']
	text_array = get_message_text_array(message)

	if len(text_array) > 1:
		user_id = text_array[1]
		if raise_invalid_id(user_id, update):
			if check_in_blacklist(conn, user_id):
				update.message.reply_text(in_blacklist_text)
			else:
				update.message.reply_text(not_in_blackilist_text)

	else:
		update.message.reply_text(check_text)


def count_users_blacklist(update: Update, context: CallbackContext) -> None:
	count = count_blacklist(conn)
	text = f'В черном списке {count} пользователей'
	update.message.reply_text(text)
