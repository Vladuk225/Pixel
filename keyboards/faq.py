from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def faq_kb(user_id: int, _):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("support"), callback_data=f"support:{user_id}")],
        [InlineKeyboardButton(text=_("rules"), callback_data=f"rules:{user_id}")],
        [InlineKeyboardButton(text=_("links"), callback_data=f"links:{user_id}")],
        [InlineKeyboardButton(text=_("stats"), callback_data=f"stats:{user_id}")],
        [InlineKeyboardButton(text=_("info"), callback_data=f"info:{user_id}")],
        [InlineKeyboardButton(text=_("back"), callback_data=f"back_to_info:{user_id}")],
    ])

    return keyboard


def back_to_faq_menu_kb(user_id: int, _):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("back"), callback_data=f"faq:{user_id}")]
    ])
    return keyboard