from telegram import Update
from telegram.error import Unauthorized
from telegram.ext import CallbackContext

from commands.utils import bot, form_permission
from db.operations import count_blacklist, remove_user, select_users_by_role


def mailing(update: Update, context: CallbackContext):

	message_dict = update.to_dict()['message']
	message = message_dict['text']
	mailing_text = message[9:]

	users_ids = form_permission(['user', 'admin'])
	permissions = form_permission(['admin', 'superadmin'])

	from_id = message_dict['from']['id']

	if from_id in permissions:
		for user in users_ids:
			try:
				bot.send_message(chat_id=user, text=mailing_text)
			except Unauthorized:
				remove_user(user)


def sub(update: Update, context: CallbackContext):

	message_dict = update.to_dict()['message']

	permissions = form_permission(['admin', 'superadmin'])
	from_id = message_dict['from']['id']

	if from_id in permissions:
		users = len(select_users_by_role('user'))
		admins = len(select_users_by_role('admin'))
		superadmins = len(select_users_by_role('superadmin'))
		blacklist = count_blacklist()
		update.message.reply_text(
			f'В черном списке: {blacklist}\nПользователей: {users}\nАдминов: {admins}\nСуперадминов: {superadmins}')
