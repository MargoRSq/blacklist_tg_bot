from telegram import Update
from telegram.ext import CallbackContext

from utils.instances import Message
from utils.tools import bot
from db.schemas import Blacklist
from db.operations import (
    check_in_blacklist,
    select_chat_id,
    select_message_id)


def hate(update: Update, context: CallbackContext):
    message = Message(update)

    if check_in_blacklist(message.sender_id):
        blacklist_chat_id = select_chat_id(message.sender_id)
        blacklist_message_id = select_message_id(message.sender_id)
        update.message.reply_text("Чел в черном списке!")
        message = bot.forward_message(
            message.chat_id, blacklist_chat_id, blacklist_message_id)
