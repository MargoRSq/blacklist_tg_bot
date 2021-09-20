from sqlalchemy.sql.expression import text
from telegram import Update, KeyboardButton, KeyboardButtonPollType, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

from db.operations import (insert_user,
						check_in_users,
						get_user_role)

start_superadmin = """Комманды:
	/help - вся информация о командах
	/check {user_id} - Проверить id на наличие в блэк листах
	Пример: /check 88888888

	/add {user_id} {url} - Добавить или обновить ссылку на человека
	Пример: /add 88888888 @trololo

	/remove {user_id} - Удалить человека из базы данных
	Пример: /remove 88888888

	/mailing {message} - отправить все сообщения для юзеров из базы
	/sub - количество подписчиков
	/add_admin {user_id} добавить админа
	/remove_admin {user_id} удалить админа
	/parser команда парсит все id в blacklist, которые упоминались в чате
		"""

start_admin = """Комманды:

	/help - вся информация о командах
	/check {user_id} - Проверить id на наличие в блэк листах
	Пример: /check 88888888

	/add {user_id} {url} - Добавить или обновить ссылку на человека
	Пример: /add 88888888 @trololo

	/remove {user_id} - Удалить человека из базы данных
	Пример: /remove 88888888

	/mailing {message} - отправить все сообщения для юзеров из базы
	/sub - количество подписчиков
	"""

start_user = """
	Комманды:
	/help - вся информация о командах
	/check {user_id} - Проверить id на наличие в блэк листах
	Пример: /check 88888888
	"""


user_keyboard = [['/check', '/request']]

admin_keyboard = [['/check', '/request'], 
					['/add', '/remove'], 
					['/mailing', '/sub']]

superadmin_keyboard = [['/check', '/request'], 
					['/add', '/remove'], 
					['/mailing', '/sub'],
					['/add_admin', '/remove_admin'],
					['/parser']]

reply_markup = [ReplyKeyboardMarkup(kb) for kb in [user_keyboard, admin_keyboard, superadmin_keyboard]]



def start(update: Update, context: CallbackContext) -> None:
	user = update.effective_user
	user_id = user['id']
	username = '@' + user['username']

	if not check_in_users(user_id):
		insert_user(user_id, "user", username)
		return update.message.reply_text(start_user)

	role = get_user_role(user_id)
	if role == "user":
		update.message.reply_text(start_user, reply_markup=reply_markup[0])
	elif role == "admin":
		update.message.reply_text(start_admin, reply_markup=reply_markup[1])
	elif role == "superadmin":
		update.message.reply_text(start_superadmin, reply_markup=reply_markup[2])
