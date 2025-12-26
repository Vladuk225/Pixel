from aiogram import types
from aiogram.filters import BaseFilter

class TextStartsWith(BaseFilter):
    def __init__(self, prefix: str):
        self.prefix = prefix

    async def __call__(self, message: types.Message) -> bool:
        return bool(message.text) and message.text.startswith(self.prefix)

class CallbackDataStartsWith(BaseFilter):
    def __init__(self, prefix: str):
        self.prefix = prefix

    async def __call__(self, callback_query: types.CallbackQuery) -> bool:
        return bool(callback_query.data) and callback_query.data.startswith(self.prefix)