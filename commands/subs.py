from telegram import Update
from telegram.ext import CallbackContext

from utils.instances import Message
from db.operations import (count_blacklist, count_users_by_role,
						set_state,
						form_ids_list,
						count_users_by_role)
from db.schemas import State


def mailing(update: Update, context: CallbackContext):

	message = Message(update)
	permissions = form_ids_list(['admin', 'superadmin'])

	if message.len == 1 and message.sender_id in permissions:
		update.message.reply_text('Введите сообщение, которое рассмотрят администраторы!')
		set_state(user=message.sender_id, st=State.waiting4mailing)



def sub(update: Update, context: CallbackContext):

	message = Message(update)
	permissions = form_ids_list(['admin', 'superadmin'])

	if message.sender_id in permissions:
		users = count_users_by_role('user')
		admins = count_users_by_role('admin')
		superadmins = count_users_by_role('superadmin')
		blacklist = count_blacklist()
		update.message.reply_text(
			f'В черном списке: {blacklist}\nПользователей: {users}\nадминистраторов: {admins}\nСуперадминистраторов: {superadmins}')

def request(update: Update, context: CallbackContext):
	message = Message(update)

	if message.len == 1:
		update.message.reply_text('Введите сообщение, которое рассмотрят администраторы!')
		set_state(user=message.sender_id, st=State.waiting4request)
