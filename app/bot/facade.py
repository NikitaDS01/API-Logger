import logging

from telebot import TeleBot


class LogBot:
    def __init__(self, token: str, chat_id: str) -> None:
        self.bot = TeleBot(token=token)
        self.chat_id = chat_id

    def send_message(
            self, message: str, parse_mode='HTML'
        ) -> None:
        self.bot.send_message(
            chat_id=self.chat_id,
            text=message,
            parse_mode=parse_mode
        )
    
    def send_document(
            self, message: str, document, 
            parse_mode='HTML',
            file_name: str|None = None
    ) -> None:
        if file_name is None:
            self.bot.send_document(
                chat_id=self.chat_id,
                caption=message,
                document=document,
                parse_mode=parse_mode
            )
        else:
            self.bot.send_document(
                chat_id=self.chat_id,
                caption=message,
                visible_file_name=file_name,
                document=document,
                parse_mode=parse_mode
            )