from telegram import Update, user
from telegram.ext import CallbackContext

from utils.config import ADMIN_FILE, SUPERUSERS_FILE

from commands.utils import add_user, remove_user


lines_admin = open(ADMIN_FILE, 'r').readlines()
admins = [line.rstrip() for line in lines_admin]

superusers_lines = open(SUPERUSERS_FILE, 'r').readlines()
superusers = [line.rstrip() for line in superusers_lines]


def append_user_admin(update: Update, context: CallbackContext) -> None:
    global admins, superusers

    update_dict = update.to_dict()
    message = update_dict['message']

    text = message['text']
    user_id = text.split()[1]

    from_id = message['from']['id']
    if (from_id in superusers) and (user_id not in admins):
        admins = add_user(admins, ADMIN_FILE, user_id)
        update.message.reply_text(f'Пользователь {user_id} теперь админ!')
    elif (from_id in superusers) and (user_id in admins):
        update.message.reply_text(
            f'Пользователь {user_id} уже админ!')
    elif (from_id not in superusers):
        update.message.reply_text(
            f'Вы не админ!')


def remove_user_admin(update: Update, context: CallbackContext) -> None:
    global admins, superusers

    update_dict = update.to_dict()
    message = update_dict['message']

    text = message['text']
    user_id = text.split()[1]

    from_id = message['from']['id']
    if (from_id in superusers) and (user_id in admins):
        admins = remove_user(admins, ADMIN_FILE, user_id)
        update.message.reply_text('Админ удален!')
    elif (from_id in superusers) and (user_id not in admins):
        update.message.reply_text(
            f'Пользователь {user_id} не админ!')
    elif (from_id not in superusers):
        update.message.reply_text(
            f'Вы не админ!')
