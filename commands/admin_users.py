from db.schemas import Blacklist


from db.operations import (
    insert_user,
    remove_user
)
from commands.utils import (get_message_text_array, raise_invalid_id,
                            form_permission, check_digit,
                            admin, superadmin)
from telegram.ext import CallbackContext
from telegram import Update


added_admin_text = 'Пользователь теперь админ!'
removed_admin_text = 'Пользователь больше не админ!'
already_admin_text = 'Пользователь уже админ!'
not_admin_text = 'Пользователь не админ!'


no_permission = 'У вас недостаточно прав!'

conn = 1
def append_user_admin(update: Update, context: CallbackContext) -> None:

    update_dict = update.to_dict()
    message = update_dict['message']
    text_array = get_message_text_array(message)

    if len(text_array) >= 2:
        user_id = text_array[1]
        raise_invalid_id(user_id, update)

        url = ''
        if len(text_array) > 2:
            url = text_array[1]

        permissions = form_permission([superadmin])
        permissions_dict = permissions['dict']

        superadmins = permissions_dict[superadmin]

        from_id = message['from']['id']

        if from_id in superadmins:
            result = insert_user(user_id, admin, url)
            if result:
                update.message.reply_text(added_admin_text)
            else:
                update.message.reply_text(already_admin_text)

        elif from_id not in superadmins:
            update.message.reply_text(no_permission)


def remove_user_admin(update: Update, context: CallbackContext) -> None:

    update_dict = update.to_dict()
    message = update_dict['message']
    text_array = get_message_text_array(message)

    if len(text_array) > 1:
        user_id = text_array[1]
        raise_invalid_id(user_id, update)

        permissions = form_permission([superadmin])
        permissions_dict = permissions['dict']

        superadmins = permissions_dict[superadmin]

        from_id = message['from']['id']

        if from_id in superadmins:
            result = remove_user(user_id)
            if result:
                update.message.reply_text(removed_admin_text)
            else:
                update.message.reply_text(not_admin_text)

        elif (from_id not in superadmins):
            update.message.reply_text(no_permission)
