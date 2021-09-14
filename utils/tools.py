from telegram import bot

from utils.config import TOKEN

bot = bot.Bot(token=TOKEN)


def if_all_digits(string):
    return all([c.isdigit() for c in string]) and len(string) < 11
