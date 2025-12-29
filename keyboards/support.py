from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def finish_report_kb(user_id, _):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("support_finish"), callback_data=f'support_finish:{user_id}')],
        [InlineKeyboardButton(text=_("back"), callback_data=f'faq:{user_id}')]
    ])
    return keyboard