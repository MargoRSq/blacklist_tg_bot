from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from utils.config import TOKEN
from commands.admin_users import append_user_admin, remove_user_admin
from commands.blacklist_users import append_user_blacklist, remove_user_blacklist, check_user_blacklist

from pprint import pprint


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Привет, {user.mention_markdown_v2()}, что прикажешь?\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(CommandHandler("admin", append_user_admin))
    dispatcher.add_handler(CommandHandler(
        "remove_admin", remove_user_admin))

    dispatcher.add_handler(CommandHandler("add", append_user_blacklist))
    dispatcher.add_handler(CommandHandler("remove", remove_user_blacklist))
    dispatcher.add_handler(CommandHandler("check", check_user_blacklist))

    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, add_user_blacklist))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
