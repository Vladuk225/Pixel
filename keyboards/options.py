from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def options_kb(user_id: int, _):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("notifications"), callback_data=f"notifications:{user_id}")],
        [InlineKeyboardButton(text=_("language"), callback_data=f"language:{user_id}")],  
        [InlineKeyboardButton(text=_("back"), callback_data=f"back_to_info:{user_id}")]
    ])

    return keyboard