from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def shop_kb(user_id, _):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{_('bonus_btn_text')} 2", callback_data=f"bonus2_info:{user_id}")],
        [InlineKeyboardButton(text=f"{_('bonus_btn_text')} 3", callback_data=f"bonus2_info:{user_id}")],
        [InlineKeyboardButton(text=_("back"), callback_data=f"back_to_info:{user_id}")]
    ])
    return kb


def bonus_buy_kb(user_id, _, num):
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("shop_buy_btn"), callback_data=f"buy_bonus_{num}:{user_id}")],
        [InlineKeyboardButton(text=_("back"), callback_data=f"shop:{user_id}")]
    ])
    return kb