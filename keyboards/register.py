from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.user import User


async def get_register_keyboard(user_id: int, _):
    user = await User.get(user_id)
    if not user:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=_( "register_btn" ), callback_data=f"register_user:{user_id}")]
        ])
        return keyboard
    return None


def get_register_select_gender_keyboard(user_id: int, _):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"👦 {_('male')}", callback_data=f"gender_male:{user_id}")],
        [InlineKeyboardButton(text=f"👧 {_('female')}", callback_data=f"gender_female:{user_id}")],
    ])
    return keyboard