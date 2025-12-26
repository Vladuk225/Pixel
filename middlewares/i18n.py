import json
from aiogram.types import TelegramObject
from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from database.lang import UserLanguageDB


class I18nMiddleware(BaseMiddleware):
    def __init__(self, locales_path: str = "locales"):
        self.locales_path = locales_path
        self.translations = {
            lang: json.load(open(f"{locales_path}/{lang}.json", encoding="utf-8"))
            for lang in ["en", "ru"]
        }

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        lang_code = await UserLanguageDB().get_language(user.id)
        translations = self.translations.get(lang_code, self.translations["en"])
        def _(key: str) -> str:
            return translations.get(key, key)

        data["_"] = _
        return await handler(event, data)

    async def get_localizer_for_user(self, user_id: int) -> Callable[[str], str]:
        lang_code = await UserLanguageDB().get_language(user_id)
        translations = self.translations.get(lang_code, self.translations["en"])

        def _(key: str) -> str:
            return translations.get(key, key)

        return _