from utils.db import conn


class InvalidId(Exception):
    pass


def check_digit(string):
    if all([c.isdigit() for c in string]):
        return True
    else:
        raise InvalidId('invalid id')


def get_message_text_array(message):
    text = message['text']
    return text.split()


def raise_invalid_id(user_id, update):
    try:
        check_digit(user_id)
    except InvalidId:
        update.message.reply_text(
            'Ошибка! введите правильный ID пользователя!')
