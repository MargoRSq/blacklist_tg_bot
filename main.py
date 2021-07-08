from telegram import Update, ForceReply, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.utils.helpers import from_timestamp

from utils.config import TOKEN
from commands.subs import mailing, sub
from commands.start import start
from commands.admin_users import append_user_admin, remove_user_admin
from commands.blacklist_users import append_user_blacklist, remove_user_blacklist, check_user_blacklist


from pprint import pprint
from psycopg2.errors import SyntaxError


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(CommandHandler("add_admin", append_user_admin))
    dispatcher.add_handler(CommandHandler(
        "remove_admin", remove_user_admin))

    dispatcher.add_handler(CommandHandler("add", append_user_blacklist))
    dispatcher.add_handler(CommandHandler("remove", remove_user_blacklist))
    dispatcher.add_handler(CommandHandler("check", check_user_blacklist))
    dispatcher.add_handler(CommandHandler("mailing", mailing))
    dispatcher.add_handler(CommandHandler("sub", sub))

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
