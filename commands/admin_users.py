import re

from telegram import Update
from telegram.ext import CallbackContext

from utils.instances import Message
from utils.tools import if_all_digits
from db.schemas import UserType
from db.operations import (
    insert_user,
    remove_user,
    get_user_role,
    insert_user,
    check_in_users,
    form_ids_list
)

no_permission = 'У вас недостаточно прав!'

def append_user_admin(update: Update, context: CallbackContext) -> None:

    message = Message(update)
    permissions_list = form_ids_list(['superadmin'])

    if message.len == 2 and message.sender_id in permissions_list:
        update.message.reply_text("Введите ссылку на пользователя")
    elif message.len == 3 and message.sender_id in permissions_list:
        targer_id = message.text_array[1]
        target_url = message.text_array[2]
        if not re.findall(r'\@\w+', message.text):
            return update.message.reply_text("@{username} не найден")
        if not if_all_digits(targer_id):
            return update.message.reply_text("Некорректный ID")

        result = insert_user(
            user=targer_id, url=target_url, role=UserType.admin)
        if result:
            update.message.reply_text('Пользователь теперь админ!')
    else:
        update.message.reply_text(no_permission)


def remove_user_admin(update: Update, context: CallbackContext) -> None:

    message = Message(update)
    permissions_list = form_ids_list(['superadmin'])

    if message.len == 2 and message.sender_id in permissions_list:
        targer_id = message.text_array[1]
        if not if_all_digits(targer_id):
            return update.message.reply_text("Некорректный ID")
        if not check_in_users(targer_id):
            return update.message.reply_text("Пользователь и так не админ")

        role = get_user_role(message.sender_id)
        if role >= UserType.superadmin.value:
            remove_user(targer_id)
            update.message.reply_text("Пользователь больше не админ!")
    else:
        update.message.reply_text(no_permission)
