from starlette.config import Config

BLACKLIST_FILE = 'blacklist.txt'

ADMIN_FILE = 'admin.txt'

SUPERUSERS_FILE = 'superusers.txt'

config = Config(".env")

TOKEN: str = config("TOKEN")

DB_NAME: str = config("DB_NAME")
DB_USER: str = config("DB_USER")
DB_PASSWORD: str = config("DB_PASSWORD")
