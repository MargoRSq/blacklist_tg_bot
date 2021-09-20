import re

from telegram import Update
from telegram.ext import CallbackContext

from utils.instances import Message
from utils.tools import if_all_digits
from db.schemas import Blacklist, State
from db.operations import (
    check_in_blacklist,
    insert_to_blacklist,
    remove_from_blacklist,
    get_user_role,
    select_from_blacklist,
    form_ids_list,
    set_state
)
from commands.hater import hello

no_permission = 'У вас недостаточно прав!'


def append_user_blacklist(update: Update, context: CallbackContext) -> None:

    message = Message(update)
    permissions_list = form_ids_list(['admin', 'superadmin'])

    if message.len == 1 and message.sender_id in permissions_list:
        update.message.reply_text("Введите id и username")
        set_state(user=message.sender_id, st=State.waiting4add)


def remove_user_blacklist(update: Update, context: CallbackContext) -> None:

    message = Message(update)
    permissions_list = form_ids_list(['admin', 'superadmin'])

    if message.len == 1 and message.sender_id in permissions_list:
        update.message.reply_text('Введите id пользователя')
        set_state(user=message.sender_id, st=State.waiting4remove)


def check_user_blacklist(update: Update, context: CallbackContext) -> None:

    message = Message(update)

    if message.len == 1:
        update.message.reply_text('Введите id пользователя!')
        set_state(user=message.sender_id, st=State.waiting4check)