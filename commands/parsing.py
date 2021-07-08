import re

from telegram import Bot, ForceReply, Update
from telegram.ext import CallbackContext, CommandHandler, Updater, jobqueue

from utils.db import conn, insert_to_blacklist, check_in_blacklist


def parse_ids(update: Update, context: CallbackContext):
    update_dict = update.to_dict()
    message = update_dict['message']

    if message['chat']['type'] == 'group':
        text = message['text']
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
