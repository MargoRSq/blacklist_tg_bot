from telegram import Update
from telegram.error import Unauthorized
from telegram.ext import CallbackContext

from utils.instances import Message
from utils.tools import bot
from db.operations import (count_blacklist, count_users_by_role,
						remove_user,
						set_state,
						form_ids_list,
						count_users_by_role)
from db.schemas import State


def mailing(update: Update, context: CallbackContext):

	message = Message(update)
	mailing_text = message.text[9:]

	users_ids = form_ids_list(['user', 'admin'])
	permissions = form_ids_list(['admin', 'superadmin'])

	if message.sender_id in permissions:
		for user in users_ids:
			try:
				bot.send_message(chat_id=user, text=mailing_text)
			except Unauthorized:
				remove_user(user)


def sub(update: Update, context: CallbackContext):

	message = Message(update)
	permissions = form_ids_list(['admin', 'superadmin'])

	if message.sender_id in permissions:
		users = count_users_by_role('user')
		admins = count_users_by_role('admin')
		superadmins = count_users_by_role('superadmin')
		blacklist = count_blacklist()
		update.message.reply_text(
			f'В черном списке: {blacklist}\nПользователей: {users}\nАдминов: {admins}\nСуперадминов: {superadmins}')

def request(update: Update, context: CallbackContext):
	message = Message(update)

	if message.len == 1:
		update.message.reply_text('Введите сообщение, которое полетит админам!')
		set_state(user=message.sender_id, st=State.waiting4request)
