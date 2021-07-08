from telegram import Update
from telegram.ext import CallbackContext


from utils.db import conn, insert_user, check_in_users

start_superadmin = """Комманды:

/start - вся информация о командах

/check {user_id} - Проверить id на наличие в блэк листах
Пример: /check 88888888

/add {user_id} {url} - Добавить или обновить ссылку на человека
Пример: /add 88888888 https://www.t.me...

/remove {user_id} - Удалить человека из базы данных
Пример: /remove 88888888

/mailing {message} - отправить все сообщения для юзеров из базы

/sub - количество подписчиков

/add_admin {user_id} добавить админа

/remove_admin {user_id} удалить админа

/parser команда парсит все id в blacklist, которые упоминались в чате
    """


start_admin = """Комманды:

/start - вся информация о командах

/check {user_id} - Проверить id на наличие в блэк листах
Пример: /check 88888888

/add {user_id} {url} - Добавить или обновить ссылку на человека
Пример: /add 88888888 https://www.t.me...

/remove {user_id} - Удалить человека из базы данных
Пример: /remove 88888888

/mailing {message} - отправить все сообщения для юзеров из базы

/sub - количество подписчиков
"""

start_user = """
Комманды:

/start - вся информация о командах

/check {user_id} - Проверить id на наличие в блэк листах
Пример: /check 88888888
"""


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    user_id = user['id']

    if_in_users = check_in_users(conn, user_id)
    if not if_in_users:
        insert_user(conn, user_id, 'user', '')
        update.message.reply_text(start_user)

    elif if_in_users['role'] == 'user':
        update.message.reply_text(start_user)

    elif if_in_users['role'] == 'admin':
        update.message.reply_text(start_admin)

    elif if_in_users['role'] == 'superadmin':
        update.message.reply_text(start_superadmin)
