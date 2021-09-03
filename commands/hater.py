from telegram import Update
from telegram.ext import CallbackContext

from commands.utils import bot

from utils.db import check_in_blacklist, conn


def hate(update: Update, context: CallbackContext):
    update_dict = update.to_dict()
    message = update_dict['message']

    user_id = message['from']['id']
    chat_id = message['chat']['id']
    new_members = message['new_chat_members']

    for user in new_members:
        if check_in_blacklist(conn, user['id']):
            bot.send_photo(chat_id=chat_id, photo=open('hi.jpg', 'rb'))
            bot.send_message(chat_id=chat_id, text='ЗДАРОВА ЛОХ')

    if check_in_blacklist(conn, user_id):
        bot.send_photo(chat_id=chat_id, photo=open('hi.jpg', 'rb'))
        update.message.reply_text('ЗДАРОВА ЛОХ')
