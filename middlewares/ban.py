from aiogram.types import Message
from aiogram import BaseMiddleware
from database.user import BanDatabase
import time


class BanMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        ban = await BanDatabase.get_ban(event.from_user.id)
        if ban:
            _, until = ban
            if time.time() < until:
                return
            else:
                await BanDatabase.unban_user(event.from_user.id)
        await handler(event, data)