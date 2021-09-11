import re

from telegram import Update
from telegram.ext import CallbackContext
from telegram.error import BadRequest

from db.operations import check_in_blacklist, insert_to_blacklist, select_users_by_role
from commands.utils import bot, check_digit
from utils.config import TRASH_CHAT_ID


def add_to_db(message):

	text = message['text']
	list_of_words = text.split()
	patterns = ['id', 'id:', 'ID', 'ID:']
	indices = [index for index, element in enumerate(
		list_of_words) if element in patterns]

	list_of_ids = []
	for index in indices:
		list_of_ids.append(list_of_words[index + 1])

	chat_id = message['chat']['id']
	message_id = message['message_id']

	urls = re.findall(r'\@\w+', message['text'])
	if urls and len(urls) == len(list_of_ids):
		for i, user in enumerate(list_of_ids):
			if check_digit(user):
				if not check_in_blacklist(user):
					insert_to_blacklist(user, url=urls[i],
						added_by='admin',
						chat_id=chat_id,
						message_id=message_id)


def load_old_ids(update: Update, context: CallbackContext):
	update_dict = update.to_dict()
	message_id = update_dict['message']['message_id']
	chat_id = update_dict['message']['chat']['id']

	superadmin_id = select_users_by_role('superadmin')[0]

	bot.send_message(
		chat_id=superadmin_id,
		text=f"Начинаю сбор ID из выбранного чата ({message_id} сообщений), это может занять несколько минут")

	for ms in range(2, message_id):
		try:
			message = bot.forward_message(TRASH_CHAT_ID, chat_id, ms)
			message['message_id'] = ms
			message['chat_id'] = chat_id
			add_to_db(message)
		except BadRequest as e:
			print(e, ms)

	bot.send_message(
		chat_id=superadmin_id, text="Чат обработан!")


def parse_ids(update: Update, context: CallbackContext):
	update_dict = update.to_dict()
	message = update_dict['message']
	add_to_db(message)
