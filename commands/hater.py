from telegram import Update
from telegram.ext import CallbackContext

from utils.instances import Message
from utils.tools import if_all_digits
from db.schemas import Blacklist, ChatType
from db.operations import (
	check_in_blacklist,
	check_state,
	unset_state,
	select_from_blacklist)



def check_blacklist_message(message: Message, update: Update):
    targer_id = message.text_array[0]
    if not if_all_digits(targer_id):
        return update.message.reply_text("Некорректный ID")
    if check_in_blacklist(targer_id):
        hello(update, targer_id)
    else:
        update.message.reply_text("Пользователь не в черном списке!")
    


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

	if check_state(message.sender_id) == 1:
		check_blacklist_message(message, update)
		unset_state(message.sender_id)
