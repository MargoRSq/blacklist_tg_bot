from db.schemas import Blacklist
from telegram import Update
from telegram.ext import CallbackContext

from commands.utils import bot

from db.operations import check_in_blacklist, select_chat_id, select_message_id


def hate(update: Update, context: CallbackContext):
	update_dict = update.to_dict()
	message = update_dict['message']

	user_id = message['from']['id']
	chat_id = message['chat']['id']
	new_members = message['new_chat_members']

	for user in new_members:
		if check_in_blacklist(user['id']):
			bot.send_photo(chat_id=chat_id, photo=open('hi.jpg', 'rb'))
			bot.send_message(chat_id=chat_id, text='ЗДАРОВА ЛОХ')

	if check_in_blacklist(user_id):
		blacklist_chat_id = select_chat_id(user_id)
		blacklist_message_id = select_message_id(user_id)
		update.message.reply_text("Чел в черном списке!")
		message = bot.forward_message(
			chat_id, blacklist_chat_id, blacklist_message_id)
