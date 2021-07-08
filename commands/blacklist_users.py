from telegram import Update
from telegram.ext import CallbackContext

from commands.utils import get_message_text_array, raise_invalid_id, form_permission
from utils.db import (
    check_in_blacklist,
    conn,
    insert_to_blacklist,
    remove_from_blacklist,
    select_users_by_role,
)


def append_user_blacklist(update: Update, context: CallbackContext) -> None:

    update_dict = update.to_dict()
    message = update_dict['message']
    text_array = get_message_text_array(message)

    if len(text_array) > 1:
        user_id = text_array[1]
        if raise_invalid_id(user_id, update):
            url = ''
            if len(text_array) > 2:
                url = text_array[2]

            permissions = form_permission(['admin', 'superadmin'])
            permissions_dict = permissions['dict']
            permissions_list = permissions['list']

            superadmins = permissions_dict['superadmin']

            from_id = message['from']['id']

            if from_id in permissions_list:

                if from_id in superadmins:
                    result = insert_to_blacklist(
                        conn, user_id, url, 'superadmin')
                else:
                    result = insert_to_blacklist(conn, user_id, url, 'admin')

                if result:
                    update.message.reply_text(
                        'Пользователь добавлен в черный список!')
                else:
                    update.message.reply_text(
                        'Пользователь уже находился в черном списке, ссылка пользователя обновлена в базе данных!')

            elif from_id not in permissions_list:
                update.message.reply_text(f'У вас недостаточно прав!')


def remove_user_blacklist(update: Update, context: CallbackContext) -> None:

    update_dict = update.to_dict()
    message = update_dict['message']
    text_array = get_message_text_array(message)

    if len(text_array) > 1:
        user_id = text_array[1]
        raise_invalid_id(user_id, update)

        permissions = form_permission(['admin', 'superadmin'])
        permissions_dict = permissions['dict']
        permissions_list = permissions['list']

        superadmins = permissions_dict['superadmin']

        from_id = message['from']['id']

        if from_id in permissions_list:

            is_in_blacklist = check_in_blacklist(conn, user_id)

            if is_in_blacklist:
                added_by = is_in_blacklist['added_by']

                if added_by == 'superadmin' and from_id in superadmins:
                    result = remove_from_blacklist(conn, user_id)
                    if result:
                        update.message.reply_text(
                            'Пользователь удален из черного списка!')

                elif added_by == 'admin' and from_id in permissions_list:
                    result = remove_from_blacklist(conn, user_id)
                    if result:
                        update.message.reply_text(
                            'Пользователь удален из черного списка!')

                elif added_by == 'superadmin' and from_id not in superadmins:
                    update.message.reply_text('У вас недостаточно прав!')
            else:
                update.message.reply_text(
                    'Пользователя нет в черном списке!')


def check_user_blacklist(update: Update, context: CallbackContext) -> None:

    update_dict = update.to_dict()
    message = update_dict['message']
    text_array = get_message_text_array(message)

    if len(text_array) > 1:
        user_id = text_array[1]
        raise_invalid_id(user_id, update)

        if check_in_blacklist(conn, user_id):
            update.message.reply_text('Пользователь в черном списке!')
        else:
            update.message.reply_text('Пользователя нет в черном списке!')
