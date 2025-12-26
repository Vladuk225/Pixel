from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from typing import Callable, Awaitable


class RegisterChatMiddleware(BaseMiddleware):
    def __init__(self, db):
        super().__init__()
        self.db = db

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable],
        event: TelegramObject,
        data: dict
    ):
        chat_id = None
        chat_type = None

        if isinstance(event, Message):
            chat_id = event.chat.id
            chat_type = event.chat.type
        elif isinstance(event, CallbackQuery):
            if event.message:
                chat_id = event.message.chat.id
                chat_type = event.message.chat.type

        if chat_id is not None and chat_type != 'private':
            await self.db.add_chat(chat_id)

        return await handler(event, data)