
from utils.db import conn, insert_user


def create_db(update: Update, context: CallbackContext):

    from_id = message['from']['id']

    permissions = form_permission([superadmin])
    permissions_dict = permissions['dict']

    superadmins = permissions_dict[superadmin]
    with conn.cursor() as cursor:
        create_roles = "CREATE TYPE roles AS ENUM ('superadmin', 'admin', 'user');"
        create_users = "CREATE TABLE users(id bigint PRIMARY KEY, role roles, url VARCHAR(100));"
        create_blacklist = "CREATE TABLE blacklist(id bigint PRIMARY KEY, url VARCHAR(100), added_by roles);"

        create_array = [create_roles, create_users, create_blacklist]

        for create in create_array:
            cursor.execute(create)
        conn.commit()


create_db()
# insert_user(conn, 627775883, 'superadmin', url='@iamsvyatoslav')
