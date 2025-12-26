from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class TextEquals(BaseFilter):
    def __init__(self, value: str):
        self.value = value

    async def __call__(self, message: Message) -> bool:
        return message.text == self.value
    

class CallbackDataEquals(BaseFilter):
    def __init__(self, value: str):
        self.value = value

    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == self.value