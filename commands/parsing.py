import re

from telegram import Update
from telegram.ext import CallbackContext
from telegram.error import BadRequest

from utils.config import TRASH_CHAT_ID
from utils.instances import Message
from db.operations import check_in_blacklist, insert_to_blacklist, select_users_by_role
from utils.tools import if_all_digits, bot


def try_add_to_db(message: Message):

    patterns = ['id', 'id:', 'ID', 'ID:']
    indices = [index for index, element in enumerate(
        message.text_array) if element in patterns]

    list_of_ids = []
    for index in indices:
        list_of_ids.append(message.text_array[index + 1])

    urls = re.findall(r'\@\w+', message.text)
    if urls and len(urls) == len(list_of_ids):
        for i, user in enumerate(list_of_ids):
            if if_all_digits(user):
                if not check_in_blacklist(user):
                    insert_to_blacklist(user, url=urls[i],
                                        added_by='admin',
                                        chat_id=message.chat_id,
                                        message_id=message.message_id,
                                        chat_type=message.type,
                                        chat_name=message.chat_name)


def load_old_ids(update: Update, context: CallbackContext):

    message = Message(update)
    superadmin_id = select_users_by_role('superadmin')[0]

    bot.send_message(
        chat_id=superadmin_id,
        text=f"Начинаю сбор ID из выбранного чата ({message.message_id} сообщений), это может занять несколько минут")

    for ms in range(2, message.message_id):
        try:
            message = bot.forward_message(TRASH_CHAT_ID,
                                          message.chat_id, ms)
            message['message_id'] = ms
            message['chat_id'] = message.chat_id
            try_add_to_db(message)
        except BadRequest as e:
            print(e, ms)

    bot.send_message(
        chat_id=superadmin_id, text="Чат обработан!")


def parse_ids(update: Update, context: CallbackContext):

    message = Message(update)
    try_add_to_db(message)
