from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class IsBot(BaseFilter):
    is_bot: bool = True 

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        user = getattr(event, "from_user", None)
        return user and user.is_bot == self.is_bot