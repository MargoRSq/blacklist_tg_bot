from utils.db import conn, select_users_by_role


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
        return True
    except InvalidId:
        update.message.reply_text(
            'Ошибка! введите правильный ID пользователя!')
        return False


def form_permission(roles: list):
    permissions_dict = {}
    for role in roles:
        users = [int(user['id'])
                 for user in select_users_by_role(conn, role)]
        permissions_dict.update({role: users})

    permissions_ids_arrays = [value for item,
                              (key, value) in enumerate(permissions_dict.items())]
    permissions_ids = [
        item for sublist in permissions_ids_arrays for item in sublist]

    return_data = {'dict': permissions_dict, 'list': permissions_ids}

    return return_data
