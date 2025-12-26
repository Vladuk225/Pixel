from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def top_kb(user_id: int, _):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("back"), callback_data=f"back_to_info:{user_id}")],
    ])

    return keyboard