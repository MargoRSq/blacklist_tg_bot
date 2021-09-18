from starlette.config import Config
from re import sub

config = Config(".env")

TOKEN: str = config("TOKEN")

DATABASE_URL: str = config("SQLALCH_DATABASE_URL")
TRASH_CHAT_ID: int = int(config("TRASH_CHAT_ID"))
