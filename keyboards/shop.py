from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.bonus import BonusDB


async def shop_kb(user_id, _):
    kb_buttons = []
    bonus_db = BonusDB()
    user_bonus = await bonus_db.get_user(user_id)

    if user_bonus.get("has_b2", 0) == 0:
        kb_buttons.append([InlineKeyboardButton(
            text=f"{_('bonus_btn_text')} 2",
            callback_data=f"bonus_info_2:{user_id}"
        )])

    if user_bonus.get("has_b3", 0) == 0:
        kb_buttons.append([InlineKeyboardButton(
            text=f"{_('bonus_btn_text')} 3",
            callback_data=f"bonus_info_3:{user_id}"
        )])

    kb_buttons.append([InlineKeyboardButton(
        text=_("back"),
        callback_data=f"back_to_info:{user_id}"
    )])

    return InlineKeyboardMarkup(inline_keyboard=kb_buttons)


def bonus_buy_kb(user_id, _, num):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("shop_buy_btn"), callback_data=f"buy_bonus_{num}:{user_id}")],
        [InlineKeyboardButton(text=_("back"), callback_data=f"shop:{user_id}")]
    ])
    return kb