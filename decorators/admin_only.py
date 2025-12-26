from aiogram.types import Message
from functools import wraps
from config import admin_ids


def admin_only(func):
    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        if message.from_user.id not in admin_ids:
            return 
        return await func(message, *args, **kwargs)
    return wrapper