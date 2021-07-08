from telegram import Update
from telegram.ext import CallbackContext

from commands.utils import get_message_text_array, raise_invalid_id, form_permission
from utils.db import (
    insert_user,
    remove_user,
    conn
)


def append_user_admin(update: Update, context: CallbackContext) -> None:

    update_dict = update.to_dict()
    message = update_dict['message']
    text_array = get_message_text_array(message)

    if len(text_array) > 1:
        user_id = text_array[1]
        raise_invalid_id(user_id, update)

        url = ''
        if len(text_array) > 2:
            url = text_array[1]

        permissions = form_permission(['superadmin'])
        permissions_dict = permissions['dict']

        superadmins = permissions_dict['superadmin']

        from_id = message['from']['id']

        if from_id in superadmins:
            result = insert_user(conn, user_id, 'admin', url)
            if result:
                update.message.reply_text(
                    f'Пользователь {user_id} теперь админ!')
            else:
                update.message.reply_text(f'Пользователь {user_id} уже админ!')

        elif from_id not in superadmins:
            update.message.reply_text(
                f'Вы не суперадмин!')


def remove_user_admin(update: Update, context: CallbackContext) -> None:

    update_dict = update.to_dict()
    message = update_dict['message']
    text_array = get_message_text_array(message)

    if len(text_array) > 1:
        user_id = text_array[1]
        raise_invalid_id(user_id, update)

        permissions = form_permission(['superadmin'])
        permissions_dict = permissions['dict']

        superadmins = permissions_dict['superadmin']

        from_id = message['from']['id']

        if from_id in superadmins:
            result = remove_user(conn, user_id)
            if result:
                update.message.reply_text(
                    f'Пользователь {user_id} больше не админ!')
            else:
                update.message.reply_text(
                    f'Пользователь {user_id} не найден!')

        elif (from_id not in superadmins):
            update.message.reply_text(
                f'Вы не суперадмин!')
