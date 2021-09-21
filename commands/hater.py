import re

from telegram import Update
from telegram.error import Unauthorized
from telegram.ext import CallbackContext

from utils.instances import Message
from utils.tools import if_all_digits, bot
from db.schemas import Blacklist, ChatType, State, UserType
from db.operations import (
	form_ids_list,
	check_in_blacklist,
	check_state,
	unset_state,
	select_from_blacklist,
	remove_user,
	get_user_role,
	insert_to_blacklist,
	remove_from_blacklist,
	check_in_users,
	insert_user)


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

def remove_blacklist_message(message: Message, update: Update) -> None:
	if message.len == 1:
		targer_id = message.text_array[0]
		if not if_all_digits(targer_id):
			return update.message.reply_text("Некорректный ID")
		if not check_in_blacklist(targer_id):
			return update.message.reply_text("Пользователь не в черном списке")

		role = get_user_role(message.sender_id)
		if role >= select_from_blacklist(Blacklist.added_by, targer_id).value:
			remove_from_blacklist(targer_id)
			update.message.reply_text("Пользователь удален из черного списка")
		else:
			update.message.reply_text('Недостаточно прав!')

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
		if user != 0:
			try:
				text = message.text + \
					f'\n from {message.sender_id} - {get_user_role(message.sender_id)}'
				bot.send_message(chat_id=user, text=text)
			except Unauthorized:
				remove_user(user)


def mailing_message(message: Message, update: Update):
	users_ids = form_ids_list(['user', 'admin'])
	for user in users_ids:
		if user != 0:
			try:
				bot.send_message(chat_id=user, text=message.text)
			except Unauthorized:
				remove_user(user)

def add_admin_message(message: Message, update: Update):
	if message.len == 1:
		update.message.reply_text("Введите ссылку на пользователя")
	elif message.len == 2:
		targer_id = message.text_array[0]
		target_url = message.text_array[1]
		if not re.findall(r'\@\w+', message.text):
			return update.message.reply_text("@{username} не найден")
		if not if_all_digits(targer_id):
			return update.message.reply_text("Некорректный ID")
		result = insert_user(
			user=targer_id, url=target_url, role=UserType.admin)
		if result:
			update.message.reply_text('Пользователь теперь администратор!')
	
def remove_admin_message(message: Message, update: Update):
	targer_id = message.text_array[0]
	if not if_all_digits(targer_id):
		return update.message.reply_text("Некорректный ID")
	if not check_in_users(targer_id):
		return update.message.reply_text("Пользователь и так не администратор")

	role = get_user_role(message.sender_id)
	if role >= UserType.superadmin.value:
		remove_user(targer_id)
		update.message.reply_text("Пользователь больше не администратор!")



def hello(update, user_id):
	message_id = select_from_blacklist(Blacklist.message_id, user_id)
	chat_name = select_from_blacklist(Blacklist.chat_name, user_id)
	chat_type = select_from_blacklist(Blacklist.chat_type, user_id)
	if chat_type.value == ChatType.channel.value:
		update.message.reply_text(
			f"Это скамер!\nСсылка на блэк!! https://t.me/{chat_name}/{message_id}")
	else:
		update.message.reply_text('Это скамер!\nДобавлен администратором')


def hate(update: Update, context: CallbackContext):
	message = Message(update)

	if check_in_blacklist(message.sender_id):
		hello(update, message.sender_id)
		
	if check_state(message.sender_id):
		if check_state(message.sender_id) == State.waiting4check.value:
			check_blacklist_message(message, update)
		elif check_state(message.sender_id) == State.waiting4request.value:
			request_to_admins(message, update)
		elif check_state(message.sender_id) == State.waiting4add.value:
			add_blacklist_message(message, update)
		elif check_state(message.sender_id) == State.waiting4remove.value:
			remove_blacklist_message(message, update)
		elif check_state(message.sender_id) == State.waiting4mailing.value:
			mailing_message(message, update)
		elif check_state(message.sender_id) == State.waiting4add_admin.value:
			add_admin_message(message, update)
		elif check_state(message.sender_id) == State.waiting4remove_admin.value:
			remove_admin_message(message, update)
		
		unset_state(message.sender_id)
