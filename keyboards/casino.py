from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUser


def casino_kb(user_id: int, _):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("casino_slots"), callback_data=f"slots:{user_id}")],
        [InlineKeyboardButton(text=_("casino_spin"), callback_data=f"spin:{user_id}")],
        [InlineKeyboardButton(text=_("casino_coin"), callback_data=f"flip_coin:{user_id}")],
        [InlineKeyboardButton(text=_("back"), callback_data=f"back_to_info:{user_id}")]
    ])


def flip_coin_kb(user_id: int, _):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("coin_with_players"), callback_data=f"flip_coin_with_player:{user_id}")],
        [InlineKeyboardButton(text=_("coin_with_bot"), callback_data=f"flip_coin_with_bot:{user_id}")],
        [InlineKeyboardButton(text=_("back"), callback_data=f"back_to_menu_casino:{user_id}")]
    ])


def slots_kb(user_id: int, _):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("slots_play"), callback_data=f"slots_play:{user_id}")],
        [InlineKeyboardButton(text=_("back"), callback_data=f"back_to_menu_casino:{user_id}")]
    ])


def spin_kb(user_id: int, _):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("spin_play"), callback_data=f"spin_play:{user_id}")],
        [InlineKeyboardButton(text=_("back"), callback_data=f"back_to_menu_casino:{user_id}")]
    ])


def coin_choice_kb(user_id: int, _):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=_("coin_heads"), callback_data=f"coin_choice:head:{user_id}"),  # Орёл
            InlineKeyboardButton(text=_("coin_tails"), callback_data=f"coin_choice:tail:{user_id}")   # Решка
        ],
        [InlineKeyboardButton(text=_("back"), callback_data=f"flip_coin:{user_id}")]
    ])


def coin_play_kb(user_id: int, _):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("play"), callback_data=f"coin_start:{user_id}")],
        [InlineKeyboardButton(text=_("back"), callback_data=f"flip_coin:{user_id}")]
    ])


def slots_play_kb(user_id: int, _):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("spin_start"), callback_data=f"slots_start:{user_id}")],
        [InlineKeyboardButton(text=_("back"), callback_data=f"slots:{user_id}")]
    ])


def spin_play_kb(user_id: int, _):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("spin_start"), callback_data=f"spin_start:{user_id}")],
        [InlineKeyboardButton(text=_("back"), callback_data=f"spin:{user_id}")]
    ])


def coin_result_kb(user_id: int, _):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("play_again"), callback_data=f"flip_coin_with_bot:{user_id}")],
        [InlineKeyboardButton(text=_("back"), callback_data=f"flip_coin:{user_id}")]
    ])


def slots_result_kb(user_id: int, _):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("play_again"), callback_data=f"slots_play:{user_id}")],
        [InlineKeyboardButton(text=_("back"), callback_data=f"slots:{user_id}")]
    ])


def spin_result_kb(user_id: int, _):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("play_again"), callback_data=f"spin_play:{user_id}")],
        [InlineKeyboardButton(text=_("back"), callback_data=f"spin:{user_id}")]
    ])


def choose_player_kb(_):
    return ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(
                text=_("choose_player"),
                request_user=KeyboardButtonRequestUser(
                    request_id=1,
                    user_is_bot=False
                )
            )
        ]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def pvp_invite_kb(initiator_id: int, _):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=_("accept"), callback_data=f"coin_pvp_accept:{initiator_id}"),
            InlineKeyboardButton(text=_("decline"), callback_data=f"coin_pvp_decline:{initiator_id}")
        ]
    ])


def coin_side_kb(player_id: int, _):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=_("coin_heads"), callback_data=f"coin_choice:heads:{player_id}"),
            InlineKeyboardButton(text=_("coin_tails"), callback_data=f"coin_choice:tails:{player_id}")
        ]
    ])


def get_game_settings_keyboard(statuses: dict, _):
    buttons = []
    GAME_DISPLAY_NAMES = {
        "coin": _("casino_coin"), 
        "slots": _("casino_slots"),
        "spin": _("casino_spin")
    }
    for key, value in statuses.items():
        if key == 'chat_id':
            continue

        emoji = '💚' if value else '❤️'
        display_name = GAME_DISPLAY_NAMES.get(key, key.capitalize())
        buttons.append(InlineKeyboardButton(
            text=f"{display_name} {emoji}",
            callback_data=f"game_toggle_{key}"
        ))

    inline_keyboard = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)