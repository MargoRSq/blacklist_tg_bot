import re

from telegram import Update
from telegram.ext import CallbackContext

from utils.instances import Message
from db.schemas import State
from db.operations import (
    form_ids_list,
    set_state
)

no_permission = 'У вас недостаточно прав!'

def append_user_admin(update: Update, context: CallbackContext) -> None:

    message = Message(update)
    permissions_list = form_ids_list(['superadmin'])

    if message.len == 1 and message.sender_id in permissions_list:
        update.message.reply_text('Введите id и username пользователя')
        set_state(user=message.sender_id, st=State.waiting4add_admin)


def remove_user_admin(update: Update, context: CallbackContext) -> None:

    message = Message(update)
    permissions_list = form_ids_list(['superadmin'])

    if message.len == 1 and message.sender_id in permissions_list:
        update.message.reply_text('Введите id пользователя')
        set_state(user=message.sender_id, st=State.waiting4remove_admin)

