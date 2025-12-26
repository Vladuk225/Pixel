from aiogram.types import Message, ChatMemberAdministrator, ChatMemberOwner
from aiogram.exceptions import TelegramAPIError
from functools import wraps
from utils.emojis import random_lose_emojis


def chat_admin_only():
    def decorator(handler):
        @wraps(handler)
        async def wrapper(message: Message, _, *args, **kwargs):
            if message.chat.type == "private":
                return

            try:
                member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
                if isinstance(member, (ChatMemberAdministrator, ChatMemberOwner)):
                    return await handler(message, *args, **kwargs)
                else:
                    await message.answer(f"{await random_lose_emojis()} {_( 'chat_admin_only' )}")
            except TelegramAPIError:
                await message.answer(f"{await random_lose_emojis()} TelegramAPIError")
        return wrapper
    return decorator