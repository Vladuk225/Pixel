from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery
from typing import Union


class UserIdFilter(Filter):
    async def __call__(self, obj: Union[Message, CallbackQuery]) -> int | None:
        if isinstance(obj, Message) and obj.from_user:
            return obj.from_user.id
        if isinstance(obj, CallbackQuery) and obj.from_user:
            return obj.from_user.id
        return None