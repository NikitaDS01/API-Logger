from app.bot.facade import LogBot
from config import general_cfg


bot = LogBot(
    token=general_cfg["token"],
    chat_id=general_cfg["chat_id"]
)