from telegram import Update
from telegram.ext import CallbackContext

from utils.db import (
    check_in_blacklist,
    conn,
    insert_to_blacklist,
    insert_user,
    remove_from_blacklist,
    select_users_by_role,
)


def append_user_blacklist(update: Update, context: CallbackContext) -> None:

    update_dict = update.to_dict()
    # print(update_dict)
    message = update_dict['message']
    text = message['text']
    text_array = text.split()

    user_id = text_array[1]
    url = ''
    if len(text_array) > 1:
        url = text_array[2]

    admins = [int(user['id'])
              for user in select_users_by_role(conn, 'superadmin')]
    superadmins = [int(user['id'])
                   for user in select_users_by_role(conn, 'admin')]

    permissions_list = [*admins, *superadmins]
    print(permissions_list)

    from_id = message['from']['id']

    # user_text = f'{user_id} {url}'

    if from_id in permissions_list:

        if from_id in superadmins:
            result = insert_to_blacklist(conn, user_id, url, 'superadmin')
        else:
            result = insert_to_blacklist(conn, user_id, url, 'admin')

        if result:
            update.message.reply_text('Пользователь добавлен в черный список!')
        else:
            update.message.reply_text(
                'Пользователь уже находился в черном списке, ссылка пользователя обновлена в базе данных!')

    elif from_id not in permissions_list:
        update.message.reply_text(f'У вас недостаточно прав!')


def remove_user_blacklist(update: Update, context: CallbackContext) -> None:

    update_dict = update.to_dict()
    message = update_dict['message']
    text = message['text']
    text_array = text.split()

    user_id = text_array[1]
    url = ''
    if len(text_array) > 1:
        url = text_array[1]

    admins = select_users_by_role(conn, 'superadmin')
    superadmins = select_users_by_role(conn, 'admin')

    permissions_list = [*admins, *superadmins]
    permissions_ids = [user['id'] for user in permissions_list]

    from_id = message['from']['id']

    # user_text = f'{user_id} {url}'

    if from_id in permissions_ids:

        added_by = check_in_blacklist(conn, user_id)['added_by']

        if added_by == 'superadmins' and from_id in superadmins:
            result = remove_from_blacklist(conn, user_id)
            update.message.reply_text('Пользователь удален из черного списка!')
        elif added_by == 'admins' and from_id in permissions_ids:
            result = remove_from_blacklist(conn, user_id)
            update.message.reply_text('Пользователь удален из черного списка!')
        elif added_by == 'superadmins' and from_id not in superadmins:
            update.message.reply_text('У вас недостаточно прав!')


def check_user_blacklist(update: Update, context: CallbackContext) -> None:

    update_dict = update.to_dict()
    message = update_dict['message']
    text = message['text']
    text_array = text.split()

    user_id = text_array[1]

    if check_in_blacklist(conn, user_id):
        update.message.reply_text('Пользователь в черном списке!')
    else:
        update.message.reply_text('Пользователя нет в черном списке!')
