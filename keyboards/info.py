from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def info_kb(user_id: int, _):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("options"), callback_data=f"options:{user_id}"), InlineKeyboardButton(text=_("jobs"), callback_data=f"jobs:{user_id}"), InlineKeyboardButton(text=_("casino"), callback_data=f"casino:{user_id}")],
        [InlineKeyboardButton(text=_("faq"), callback_data=f"faq:{user_id}"), InlineKeyboardButton(text=_("top"), callback_data=f"top:{user_id}"), InlineKeyboardButton(text=_("bonus_btn_text"), callback_data=f"bonus_menu:{user_id}")],
        [InlineKeyboardButton(text=_("shop_btn_text"), callback_data=f"shop:{user_id}")]
    ])
    return keyboard