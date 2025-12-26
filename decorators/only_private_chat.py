from functools import wraps
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from utils.emojis import random_lose_emojis


def private_chat_only(handler):
    @wraps(handler)
    async def wrapped(event, _, *args, **kwargs):
        chat = event.message.chat if isinstance(event, CallbackQuery) else event.chat
        if chat.type != "private":
            try:
                await event.answer(f'''
{await random_lose_emojis()} {_("private_chat_only")}
                ''', show_alert=True)
            except TelegramBadRequest:
                pass
            return
        return await handler(event, *args, **kwargs)
    return wrapped