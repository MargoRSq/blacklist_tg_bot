import re

from telegram import Update
from telegram.ext import CallbackContext

from commands.utils import get_message_text_array, form_permission, check_digit, bot
from db.operations import (
	check_in_blacklist,
	insert_to_blacklist,
	remove_from_blacklist,
	count_blacklist,
	get_user_role,
	select_addedby,
	select_users_by_role,
	select_chat_id,
	select_message_id
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

	permissions_list = form_permission(['admin', 'superadmin'])
	from_id = message['from']['id']

	if len(text_array) == 1 and from_id in permissions_list:
		update.message.reply_text(add_text)
	elif len(text_array) == 2 and from_id in permissions_list:
		update.message.reply_text("Введите ссылку на пользователя")
	elif len(text_array) == 3 and from_id in permissions_list:
		targer_id = text_array[1]
		target_url = text_array[2]
		if not re.findall(r'\@\w+', message['text']):
			return update.message.reply_text("@{username} не найден")
		if not check_digit(targer_id):
			return update.message.reply_text("Некорректный ID")

		role = get_user_role(from_id)
		result = insert_to_blacklist(targer_id, target_url, role, 1, 1)
		if result:
			update.message.reply_text(added_to_blacklist_text)
		else:
			update.message.reply_text(already_in_blacklist_text)


def remove_user_blacklist(update: Update, context: CallbackContext) -> None:

	update_dict = update.to_dict()
	message = update_dict['message']
	text_array = get_message_text_array(message)

	permissions_list = form_permission(['admin', 'superadmin'])
	from_id = message['from']['id']

	if len(text_array) == 1 and from_id in permissions_list:
		update.message.reply_text(remove_text)
	elif len(text_array) == 2 and from_id in permissions_list:
		targer_id = text_array[1]
		if not check_digit(targer_id):
			return update.message.reply_text("Некорректный ID")
		if not check_in_blacklist(targer_id):
			return update.message.reply_text("Пользователь не в черном списке")

		role = get_user_role(from_id)
		if role >= select_addedby(targer_id):
			remove_from_blacklist(targer_id)
			update.message.reply_text("Пользователь удален из черного списка")
		else:
			update.message.reply_text(no_permission)


def check_user_blacklist(update: Update, context: CallbackContext) -> None:

	update_dict = update.to_dict()
	message = update_dict['message']
	chat_id = message['chat']['id']
	text_array = get_message_text_array(message)

	if len(text_array) == 1:
		update.message.reply_text(check_text)
	elif len(text_array) == 2:
		targer_id = text_array[1]
		if not check_digit(targer_id):
			return update.message.reply_text("Некорректный ID")
		if check_in_blacklist(targer_id):
			blacklist_chat_id = select_chat_id(targer_id)
			blacklist_message_id = select_message_id(targer_id)
			update.message.reply_text("Чел в черном списке!")
			message = bot.forward_message(
				chat_id, blacklist_chat_id, blacklist_message_id)
		else:
			update.message.reply_text(not_in_blackilist_text)
