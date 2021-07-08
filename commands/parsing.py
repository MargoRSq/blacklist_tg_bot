from telegram import Update
from telegram.ext import CallbackContext

from utils.db import check_in_blacklist, conn, insert_to_blacklist
from commands.utils import bot


def add_to_db(text):

    list_of_words = text.split()
    patterns = ['id', 'id:', 'ID', 'ID:']
    indices = [index for index, element in enumerate(
        list_of_words) if element in patterns]

    list_of_ids = []
    for index in indices:
        list_of_ids.append(list_of_words[index + 1])

    for user in list_of_ids:
        if all([c.isdigit() for c in user]):
            if not check_in_blacklist(conn, user):
                insert_to_blacklist(conn, user, url='', added_by='admin')


def load_old_ids(update: Update, context: CallbackContext):
    update_dict = update.to_dict()
    message_id = update_dict['message']['message_id']
    chat_id = update_dict['message']['chat']['id']

    for message in range(1, message_id):
        try:
            text = bot.forward_message(-525700374, chat_id, message).text
            add_to_db(text)
        except:
            pass


def parse_ids(update: Update, context: CallbackContext):
    update_dict = update.to_dict()
    message = update_dict['message']

    if message['chat']['type'] == 'group':
        text = message['text']
        add_to_db(text)
