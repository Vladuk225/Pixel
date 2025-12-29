from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


LANGUAGES = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English"
}


def get_language_keyboard(current_lang: str, user_id: int, _) -> InlineKeyboardMarkup:
    buttons = []
    for lang_code, label in LANGUAGES.items():
        text = f"{label} {'💚' if lang_code == current_lang else ''}"
        buttons.append(
            [InlineKeyboardButton(text=text, callback_data=f"set_lang-{lang_code}:{user_id}")]
        )
    buttons.append(
        [InlineKeyboardButton(text=_("back"), callback_data=f'options:{user_id}')]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)