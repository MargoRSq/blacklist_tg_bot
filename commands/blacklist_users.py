from telegram import Update
from telegram.ext import CallbackContext

from commands.utils import add_user, remove_user, update_id_list

from psycopg2.errors import UniqueViolation


from utils.db import conn, select_users_by_role, insert_user, insert_to_blacklist, remove_from_blacklist


def append_user_blacklist(update: Update, context: CallbackContext) -> None:

    update_dict = update.to_dict()
    message = update_dict['message']

    admins = select_users_by_role(conn, 'superadmin')
    superadmins = select_users_by_role(conn, 'admin')

    permissions_list = [*admins, *superadmins]

    permissions_ids = [user['id'] for user in permissions_list]

    text = message['text']
    text_array = text.split()
    user_id = text_array[1]

    from_id = message['from']['id']

    url = ''
    if len(text_array) > 1:
        url = text_array[2]

    # user_text = f'{user_id} {url}'

    if from_id in permissions_ids:

        if from_id in superadmins:
            result = insert_to_blacklist(conn, user_id, url, 'superadmin')
        else:
            result = insert_to_blacklist(conn, user_id, url, 'admin')

        if result:
            update.message.reply_text('Пользователь добавлен в черный список!')
        else:
            update.message.reply_text(
                'Пользователь уже находился в черном списке, ссылка пользователя обновлена в базе данных!')

    elif from_id not in permissions_ids:
        update.message.reply_text(f'У вас недостаточно прав!')


def remove_user_blacklist(update: Update, context: CallbackContext) -> None:

    update_dict = update.to_dict()
    message = update_dict['message']

    admins = select_users_by_role(conn, 'superadmin')
    superadmins = select_users_by_role(conn, 'admin')

    permissions_list = [*admins, *superadmins]

    permissions_ids = [user['id'] for user in permissions_list]

    text = message['text']
    text_array = text.split()
    user_id = text_array[1]

    from_id = message['from']['id']

    url = ''
    if len(text_array) > 1:
        url = text_array[2]

    # user_text = f'{user_id} {url}'

    if from_id in permissions_ids:

        if from_id in superadmins:
            result = remove_from_blacklist(conn, user_id,)
        else:
            result = insert_to_blacklist(conn, user_id, url, 'admin')

        if result:
            update.message.reply_text('Пользователь добавлен в черный список!')
        else:
            update.message.reply_text(
                'Пользователь уже находился в черном списке, ссылка пользователя обновлена в базе данных!')

    elif from_id not in permissions_ids:
        update.message.reply_text(f'У вас недостаточно прав!')


# def remove_user_blacklist(update: Update, context: CallbackContext) -> None:
#     global blacklist, admins, superusers, blacklist_ids

#     update_dict = update.to_dict()
#     from_id = update_dict['message']['from']['id']

#     # permission_list = [*]
#     if str(from_id) in superusers:
#         text = update_dict['message']['text']
#         user_id = text.split()[1]

#         if user_id in blacklist_ids:
#             blacklist = remove_user(blacklist, BLACKLIST_FILE, user_id)
#             blacklist_ids = update_id_list(lines_blacklist)
#             update.message.reply_text('Пользователь удален из черного списка!')
#         else:
#             update.message.reply_text(
#                 f'Пользователь {user_id} не в черном списке!')


# def check_user_blacklist(update: Update, context: CallbackContext) -> None:
#     global blacklist

#     update_dict = update.to_dict()

#     text = update_dict['message']['text']
#     user_id = text.split()[1]

#     if user_id in blacklist_ids:
#         update.message.reply_text(
#             f'Пользователь {user_id} находится в черном списке!')
#     else:
#         update.message.reply_text(
#             f'Пользователь {user_id} не в черном списке!')
