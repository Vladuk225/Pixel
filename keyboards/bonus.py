from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def create_bonus_keyboard(user_id, user: dict, _) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    bonus_text = _("bonus_btn_text")
    builder.button(text=f"{bonus_text} 1", callback_data=f"bonus_1:{user_id}")
    if user.get("has_b2", 0) == 1:
        builder.button(text=f"{bonus_text} 2", callback_data=f"bonus_2:{user_id}")
    if user.get("has_b3", 0) == 1:
        builder.button(text=f"{bonus_text} 3", callback_data=f"bonus_3:{user_id}")
    builder.button(text=_("back"), callback_data=f"back_to_info:{user_id}")
    builder.adjust(1)
    return builder.as_markup()


async def bonus_claimed_kb(user_id, _):
    builder = InlineKeyboardBuilder()
    builder.button(text=_("back"), callback_data=f"bonus_menu:{user_id}")
    builder.adjust(1)
    return builder.as_markup()