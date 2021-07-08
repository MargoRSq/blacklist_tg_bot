from telegram import Update
from telegram.ext import CallbackContext
from telegram.error import Unauthorized

from commands.utils import bot
from commands.utils import form_permission

from utils.db import (
    conn,
    select_users_by_role,
    remove_user
)


def mailing(update: Update, context: CallbackContext):

    message_dict = update.to_dict()['message']
    message = message_dict['text']
    mailing_text = message[9:]

    users_arrays = [select_users_by_role(conn, user)
                    for user in ['user', 'admin']]

    users_dicts = [
        item for sublist in users_arrays for item in sublist]

    users_ids = [user['id'] for user in users_dicts]

    permissions = form_permission(['admin', 'superadmin'])
    permissions_list = permissions['list']

    from_id = message_dict['from']['id']

    if from_id in permissions_list:

        for user in users_ids:
            try:
                bot.send_message(chat_id=user, text=mailing_text)
            except Unauthorized:
                remove_user(conn, user)


def sub(update: Update, context: CallbackContext):

    message_dict = update.to_dict()['message']

    permissions = form_permission(['admin', 'superadmin'])
    permissions_list = permissions['list']

    from_id = message_dict['from']['id']

    if from_id in permissions_list:

        users = len(select_users_by_role(conn, 'user'))
        admins = len(select_users_by_role(conn, 'admin'))
        superadmins = len(select_users_by_role(conn, 'superadmin'))
        update.message.reply_text(
            f'Пользователей: {users}\nАдминов: {admins}\nСуперадминов: {superadmins}')
