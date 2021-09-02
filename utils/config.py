from starlette.config import Config


config = Config(".env")

TOKEN: str = config("TOKEN")

DATABASE_URL: str = config("DATABASE_URL")

TRASH_CHAT_ID: int = int(config("TRASH_CHAT_ID"))
