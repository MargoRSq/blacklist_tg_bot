import re

from telegram import Update
from telegram.ext import CallbackContext

from utils.instances import Message
from utils.tools import if_all_digits
from db.schemas import Blacklist, StateSaver, State
from db.operations import (
    check_in_blacklist,
    insert_to_blacklist,
    remove_from_blacklist,
    get_user_role,
    select_from_blacklist,
    form_ids_list,
    check_state,
    set_state
)
from commands.hater import hello

add_text = """
/add {user_id} {url} - Добавить или обновить ссылку на человека
Пример: /add 88888888 @trololo
"""
remove_text = """
/remove {user_id} - Удалить человека из базы данных
Пример: /remove 88888888
"""
check_text = """
/check {user_id} - Проверить id на наличие в блэк листах
Пример: /check 88888888
"""

no_permission = 'У вас недостаточно прав!'


def append_user_blacklist(update: Update, context: CallbackContext) -> None:

    message = Message(update)
    permissions_list = form_ids_list(['admin', 'superadmin'])

    if message.len == 1 and message.sender_id in permissions_list:
        update.message.reply_text(add_text)
    elif message.len == 2 and message.sender_id in permissions_list:
        update.message.reply_text("Введите ссылку на пользователя")
    elif message.len == 3 and message.sender_id in permissions_list:
        targer_id = message.text_array[1]
        target_url = message.text_array[2]
        if not re.findall(r'\@\w+', message.text):
            return update.message.reply_text("@{username} не найден")
        if not if_all_digits(targer_id):
            return update.message.reply_text("Некорректный ID")

        role = get_user_role(message.sender_id)
        result = insert_to_blacklist(targer_id, target_url,
                                     role, message.chat_id,
                                     message.message_id,
                                     chat_type=message.type,
                                     chat_name=message.chat_name)
        if result:
            update.message.reply_text('Пользователь добавлен в черный список!')
        else:
            update.message.reply_text('Пользователь уже находился в черном списке!')


def remove_user_blacklist(update: Update, context: CallbackContext) -> None:

    message = Message(update)
    permissions_list = form_ids_list(['admin', 'superadmin'])

    if message.len == 1 and message.sender_id in permissions_list:
        update.message.reply_text(remove_text)
    elif message.len == 2 and message.sender_id in permissions_list:
        targer_id = message.text_array[1]
        if not if_all_digits(targer_id):
            return update.message.reply_text("Некорректный ID")
        if not check_in_blacklist(targer_id):
            return update.message.reply_text("Пользователь не в черном списке")

        role = get_user_role(message.sender_id)
        if role >= select_from_blacklist(Blacklist.added_by, targer_id):
            remove_from_blacklist(targer_id)
            update.message.reply_text("Пользователь удален из черного списка")
        else:
            update.message.reply_text(no_permission)


def check_user_blacklist(update: Update, context: CallbackContext) -> None:

    message = Message(update)

    if message.len == 1:
        update.message.reply_text('Введите id пользователя!')
        set_state(user=message.sender_id, st=State.waiting4check)
    elif message.len == 2:
        targer_id = message.text_array[1]
        if not if_all_digits(targer_id):
            return update.message.reply_text("Некорректный ID")
        if check_in_blacklist(targer_id):
            hello(update, targer_id)
        else:
            update.message.reply_text("Пользователь не в черном списке!")
