from aiogram.filters import BaseFilter
from aiogram.types import Message
from typing import Union


class IsRegisteredFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, dict]:
        from database.user import User 

        user = await User.get(message.from_user.id)
        return user is not None