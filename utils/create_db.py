from telegram import Update
from telegram.ext import CallbackContext

from utils.db import conn, insert_user

from commands.utils import form_permission, superadmin


def create_db(update: Update, context: CallbackContext):

    update_dict = update.to_dict()
    message = update_dict['message']

    permissions = form_permission([superadmin])
    permissions_dict = permissions['dict']
    superadmins = permissions_dict[superadmin]

    from_id = message['from']['id']
    if from_id in superadmins:
        with conn.cursor() as cursor:
            create_roles = "CREATE TYPE roles AS ENUM ('superadmin', 'admin', 'user');"
            create_users = "CREATE TABLE users(id bigint PRIMARY KEY, role roles, url VARCHAR(100));"
            create_blacklist = "CREATE TABLE blacklist(id bigint PRIMARY KEY, url VARCHAR(100), added_by roles);"

            create_array = [create_roles, create_users, create_blacklist]

            for create in create_array:
                cursor.execute(create)
            conn.commit()


# create_db()
# insert_user(conn, 627775883, 'superadmin', url='@iamsvyatoslav')
