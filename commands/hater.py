import re

from telegram import Update
from telegram.error import Unauthorized, BadRequest
from telegram.ext import CallbackContext

from utils.instances import Message
from utils.tools import if_all_digits, bot
from db.schemas import Blacklist, ChatType
from db.operations import (
	form_ids_list,
	check_in_blacklist,
	check_state,
	unset_state,
	select_from_blacklist,
	remove_user,
	get_user_role,
	insert_to_blacklist)


def add_blacklist_message(message: Message, update: Update):
	permissions_list = form_ids_list(['admin', 'superadmin'])

	if message.len == 1 and message.sender_id in permissions_list:
		update.message.reply_text("Введите ссылку на пользователя")
	elif message.len == 2 and message.sender_id in permissions_list:
		targer_id = message.text_array[0]
		target_url = message.text_array[1]
		if not re.findall(r'\@\w+', message.text):
			return update.message.reply_text("@{username} не найден")
		if not if_all_digits(targer_id):
			return update.message.reply_text("Некорректный ID")

		role = get_user_role(message.sender_id)
		result = insert_to_blacklist(targer_id, target_url,
									role, message.chat_id,
									message.message_id,
									chat_type=message.type,
									chat_name=message.chat_name)
		if result:
			update.message.reply_text('Пользователь добавлен в черный список!')
		else:
			update.message.reply_text('Пользователь уже находился в черном списке!')


def check_blacklist_message(message: Message, update: Update):
	targer_id = message.text_array[0]
	if not if_all_digits(targer_id):
		return update.message.reply_text("Некорректный ID")
	if check_in_blacklist(targer_id):
		hello(update, targer_id)
	else:
		update.message.reply_text("Пользователь не в черном списке!")


def request_to_admins(message: Message, update: Update):
	send_list = form_ids_list(['admin'])[:-1]
	for user in send_list:
		try:
			text = message.text + \
				f'\n from {message.sender_id} - {get_user_role(message.sender_id)}'
			bot.send_message(chat_id=user, text=text)
		except Unauthorized:
			remove_user(user)




def hello(update, user_id):
	message_id = select_from_blacklist(Blacklist.message_id, user_id)
	chat_name = select_from_blacklist(Blacklist.chat_name, user_id)
	chat_type = select_from_blacklist(Blacklist.chat_type, user_id)
	if chat_type.value == ChatType.channel.value:
		update.message.reply_text(
			f"Внимание! Чел кидок!\nhttps://t.me/{chat_name}/{message_id}")
	else:
		update.message.reply_text('Внимание! Чел кидок!')


def hate(update: Update, context: CallbackContext):
	message = Message(update)

	if check_in_blacklist(message.sender_id):
		hello(update, message.sender_id)
	elif check_state(message.sender_id) == 1:
		check_blacklist_message(message, update)
		unset_state(message.sender_id)
	elif check_state(message.sender_id) == 2:
		request_to_admins(message, update)
		unset_state(message.sender_id)
	elif check_state(message.sender_id) == 3:
		add_blacklist_message(message, update)
		unset_state(message.sender_id)
	# elif check_state(message.sender_id) == 4:
	# 	request_to_admins(message, update)
	# 	unset_state(message.sender_id)