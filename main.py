from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from commands.admin_users import append_user_admin, remove_user_admin
from commands.blacklist_users import (
    append_user_blacklist,
    check_user_blacklist,
    remove_user_blacklist
)
from commands.hater import hate
from commands.parsing import load_old_ids, parse_ids
from commands.start import start
from commands.subs import mailing, sub
from commands.db import create_db
from utils.config import TOKEN


def main() -> None:
    """Start the bot."""
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))

    dispatcher.add_handler(CommandHandler("add_admin", append_user_admin))
    dispatcher.add_handler(CommandHandler(
        "remove_admin", remove_user_admin))

    dispatcher.add_handler(CommandHandler("add", append_user_blacklist))
    dispatcher.add_handler(CommandHandler("remove", remove_user_blacklist))
    dispatcher.add_handler(CommandHandler("check", check_user_blacklist))
    dispatcher.add_handler(CommandHandler("mailing", mailing))
    dispatcher.add_handler(CommandHandler("sub", sub))

    dispatcher.add_handler(CommandHandler("parser", load_old_ids))
    dispatcher.add_handler(CommandHandler("create_db", create_db))

    dispatcher.add_handler(MessageHandler(
        Filters.regex('(id|id:|ID)'), parse_ids))
    dispatcher.add_handler(MessageHandler(Filters.regex('.*'), hate))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
