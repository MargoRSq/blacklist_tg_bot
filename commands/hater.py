from telegram import Update
from telegram.ext import CallbackContext

from utils.instances import Message
from utils.tools import bot
from db.schemas import Blacklist, ChatType
from db.operations import (
	check_in_blacklist,
	select_from_blacklist)


def hello(update, user_id):
	message_id = select_from_blacklist(Blacklist.message_id, user_id)
	chat_name = select_from_blacklist(Blacklist.chat_name, user_id)
	chat_type = select_from_blacklist(Blacklist.chat_type, user_id)
	if chat_type.value == ChatType.channel.value:
		update.message.reply_text(
			f"Внимание! Чел кидок!\nhttps://t.me/{chat_name}/{message_id}")
	else:
		update.message.reply_text('Внимание! Чел кидок!')


def hate(update: Update, context: CallbackContext):
	message = Message(update)

	if check_in_blacklist(message.sender_id):
		hello(update, message.sender_id)
