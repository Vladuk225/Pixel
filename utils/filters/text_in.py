from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class TextIn(BaseFilter):
    def __init__(self, values: list[str]):
        self.values = [v.lower() for v in values]

    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False
        text = message.text.lower()
        return any(text.startswith(v) for v in self.values)
    

class CallbackDataIn(BaseFilter):
    def __init__(self, values: list[str]):
        self.values = [v.lower() for v in values]

    async def __call__(self, callback: CallbackQuery) -> bool:
        if not callback.data:
            return False
        data = callback.data.lower()
        return any(data.startswith(v) for v in self.values)