from telegram import bot

from utils.config import TOKEN
from db.operations import select_users_by_role


admin = 'admin'
superadmin = 'superadmin'
user = 'user'


bot = bot.Bot(token=TOKEN)


class InvalidId(Exception):
	pass


def check_digit(string):
	return all([c.isdigit() for c in string]) and len(string) < 11


def get_message_text_array(message):
	text = message['text']
	return text.split()


def raise_invalid_id(user_id, update):
	try:
		check_digit(user_id)
		return True
	except InvalidId:
		update.message.reply_text(
			'Ошибка! введите правильный ID пользователя!')
		return False


def form_permission(roles: list):
	permissions_list = []
	for role in roles:
		permissions_list.extend(select_users_by_role(role))
	return permissions_list
