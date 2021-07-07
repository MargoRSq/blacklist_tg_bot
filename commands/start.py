from telegram import Update
from telegram.ext import CallbackContext

from psycopg2.errors import UniqueViolation, InFailedSqlTransaction

from utils.db import conn, insert_user, select_users_by_role, check_in_blacklist, check_in_users


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    user_id = user['id']
    update.message.reply_markdown_v2(
        fr'Привет, {user.mention_markdown_v2()}, что прикажешь?\!'
    )
    # try:
    if_in_users = check_in_users(conn, user_id)
    if not if_in_users:
        insert_user(conn, user_id, 'user', '')
    # except (UniqueViolation, InFailedSqlTransaction):
    #     pass

    # print(select_users_by_role(conn, 'superadmin'))
