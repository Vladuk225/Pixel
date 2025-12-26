from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Awaitable, Dict, Any
import aiosqlite
from datetime import datetime


class LastActiveMiddleware(BaseMiddleware):
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        user = getattr(event, "from_user", None)

        if user:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "UPDATE users SET last_active = ? WHERE telegram_id = ?",
                    (datetime.now().isoformat(sep=' ', timespec='seconds'), user.id)
                )
                await db.commit()

        return await handler(event, data)