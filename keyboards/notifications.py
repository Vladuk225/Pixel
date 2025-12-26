from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def notifications_kb(allow_transfers: int, user_id: int, _) -> InlineKeyboardMarkup:
    if allow_transfers:
        text = "💰 " + _("transfer") + " 💚"
    else:
        text = "💰 " + _("transfer") + " ❤️"
    button = InlineKeyboardButton(text=text, callback_data=f"toggle_transfers:{user_id}")
    back = InlineKeyboardButton(text=_("back"), callback_data=f"options:{user_id}")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button], [back]])
    return keyboard