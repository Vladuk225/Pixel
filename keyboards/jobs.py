from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def jobs_kb(user_id: int, _):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("tik_tok_blogger_btn"), callback_data=f"tik_tok_blogger:{user_id}")],
        [InlineKeyboardButton(text=_("back"), callback_data=f"back_to_info:{user_id}")],
    ])

    return keyboard


def tik_tok_kb(user_id: int, _):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("tik_tok_video_btn_text"), callback_data=f"tik_tok_video:{user_id}"), InlineKeyboardButton(text=_("tik_tok_ad_btn_text"), callback_data=f"tik_tok_ad:{user_id}")],
        [InlineKeyboardButton(text=_("tik_tok_change_name_btn_text"), callback_data=f"tik_tok_change_name:{user_id}"), InlineKeyboardButton(text=_("tik_tok_delete_btn_text"), callback_data=f"tik_tok_delete:{user_id}")],
        [InlineKeyboardButton(text=_("back"), callback_data=f'jobs:{user_id}')]
    ])
    return keyboard


def back_to_tik_tok_menu_kb(user_id: int, _):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("back"), callback_data=f'tik_tok_blogger:{user_id}')]
    ])
    return keyboard


def confirm_delete_kb(user_id: int, _):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("yes"), callback_data=f"tik_tok_confirm_delete:yes:{user_id}")],
        [InlineKeyboardButton(text=_("no"), callback_data=f"tik_tok_confirm_delete:no:{user_id}")]
    ])


def back_to_jobs_menu_kb(user_id: int, _):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("back"), callback_data=f'jobs:{user_id}')]
    ])
    return keyboard