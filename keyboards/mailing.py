from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def get_target_select_kb(targets: set[str], user_id: int, _) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=("✅ " if "users" in targets else "") + "👤 " + _("users"),
        callback_data=f"target_users:{user_id}"
    )
    builder.button(
        text=("✅ " if "chats" in targets else "") + "👥 " + _("chats"),
        callback_data=f"target_chats:{user_id}"
    )
    builder.button(
        text=f"✅ {_('done')}",
        callback_data=f"target_done:{user_id}"
    )
    builder.adjust(2, 1)

    return builder.as_markup()