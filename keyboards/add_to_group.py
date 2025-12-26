from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot_username


def add_to_group_keyboard(_) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=_("add_to_group_btn"),
                url=f"https://t.me/{bot_username.replace('@', '')}?startgroup=true"
            )
        ]
    ])