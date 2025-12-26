from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from utils.unauthorized_messages import get_random_unauthorized_message
from keyboards.casino import slots_kb, slots_play_kb, slots_result_kb
import random
from aiogram.fsm.context import FSMContext
from states.casino import SlotsGame
from database.user import User
from handlers.users.games.main import game_check
from utils.transform import transform_int
from utils.emojis import random_lose_emojis
from database.game_settings import GameSettingsDB
from utils.filters.startswith import CallbackDataStartsWith
import asyncio
from middlewares.i18n import I18nMiddleware
import json


router = Router()
db = GameSettingsDB()
i18n_middleware = I18nMiddleware()


def get_duplicate_count(combination_text: str) -> int:
    """Подсчитывает максимальное количество повторяющихся символов в комбинации"""
    items = [i.strip() for i in combination_text.split("|")]
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    max_count = max(counts.values())
    return max_count if max_count > 1 else 0


combinations = {
    1: 3.5,      # Бар — Бар — Бар
    2: 1.2,      # Виноград — Бар — Бар
    3: 1.2,      # Лимон — Бар — Бар
    4: 1.2,      # Семёрка — Бар — Бар
    5: 0.2,      # Бар — Виноград — Бар
    6: 1.2,      # Виноград — Виноград — Бар
    9: 0.2,      # Бар — Лимон — Бар
    11: 1.2,     # Лимон — Лимон — Бар
    13: 0.2,     # Бар — Семёрка — Бар
    16: 1.5,     # Семёрка — Семёрка — Бар
    17: 1.2,     # Бар — Бар — Виноград
    18: 0.2,     # Виноград — Бар — Виноград
    21: 1.2,     # Бар — Виноград — Виноград
    22: 3.5,     # Виноград — Виноград — Виноград
    23: 1.2,     # Лимон — Виноград — Виноград
    24: 1.2,     # Семёрка — Виноград — Виноград
    26: 0.2,     # Виноград — Лимон — Виноград
    27: 1.2,     # Лимон — Лимон — Виноград
    30: 0.2,     # Виноград — Семёрка — Виноград
    32: 1.5,     # Семёрка — Семёрка — Виноград
    33: 1.2,     # Бар — Бар — Лимон
    35: 0.2,     # Лимон — Бар — Лимон
    38: 1.2,     # Виноград — Виноград — Лимон
    39: 0.2,     # Лимон — Виноград — Лимон
    41: 1.2,     # Бар — Лимон — Лимон
    42: 1.2,     # Виноград — Лимон — Лимон
    43: 3.5,     # Лимон — Лимон — Лимон
    44: 1.2,     # Семёрка — Лимон — Лимон
    47: 0.2,     # Лимон — Семёрка — Лимон
    48: 1.5,     # Семёрка — Семёрка — Лимон
    49: 1.2,     # Бар — Бар — Семёрка
    52: 0.2,     # Семёрка — Бар — Семёрка
    54: 1.2,     # Виноград — Виноград — Семёрка
    56: 0.2,     # Семёрка — Виноград — Семёрка
    59: 1.2,     # Лимон — Лимон — Семёрка
    60: 0.2,     # Семёрка — Лимон — Семёрка
    61: 1.5,     # Бар — Семёрка — Семёрка
    62: 1.5,     # Виноград — Семёрка — Семёрка
    63: 1.5,     # Лимон — Семёрка — Семёрка
    64: 10       # Семёрка — Семёрка — Семёрка
}


@router.callback_query(CallbackDataStartsWith('slots_play'))
async def slots_with_bot(call: CallbackQuery, state: FSMContext, _):
    val, user_id_str = call.data.split(":")
    user_id = int(user_id_str)

    if call.from_user.id != user_id:
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    chat_id = call.message.chat.id
    if not await db.is_game_enabled(chat_id, "slots"): # если как то тут оказались то нужно тоже блокировать
        await call.message.answer(_("slots_disabled"))
        return
    await state.set_state(SlotsGame.waiting_for_bet)
    await call.message.delete()
    await call.message.answer(_("slots_enter_bet"))


@router.message(SlotsGame.waiting_for_bet)
async def process_coin_bet(msg: Message, state: FSMContext, _):
    bet = await game_check(msg, msg.text, _)
    if not bet:
        return
    await state.update_data(bet=bet)
    await state.set_state(SlotsGame.waiting_for_play)
    await msg.answer(
        _("slots_bet_info").format(bet, bet * 10),
        reply_markup=slots_play_kb(msg.from_user.id, _),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("slots_start"))
async def start_slots_game(call: CallbackQuery, state: FSMContext, _):
    val, user_id_str = call.data.split(":")
    user_id = int(user_id_str)

    if call.from_user.id != user_id:
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)

    data = await state.get_data()
    bet = data["bet"]
    await call.message.delete()

    sent = await call.message.answer_dice(emoji='🎰')
    value = sent.dice.value
    await asyncio.sleep(1.5)

    combination = _(f"slots_combinations_{value}")
    user = await User.get(user_id_str)

    duplicates = get_duplicate_count(combination) if combination else 0
    combo_display = f"{combination} ({duplicates})" if duplicates else combination

    if value in combinations:
        multiplier = combinations.get(value)
        total_win = int(bet * multiplier)
        net_win = total_win - bet

        if total_win < bet:
            loss = bet - total_win
            await call.message.answer(
                _("slots_loss").format(combo_display, transform_int(loss)),
                reply_markup=slots_result_kb(user_id_str, _)
            )
            await user.subtract_balance(loss)
        else:
            await call.message.answer(
                _("slots_win").format(combo_display, transform_int(net_win)),
                reply_markup=slots_result_kb(user_id_str, _)
            )
            await user.add_balance(net_win)
    else:
        await call.message.answer(
            _("slots_loss").format(combo_display, transform_int(bet)),
            reply_markup=slots_result_kb(user_id_str, _)
        )
        await user.subtract_balance(bet)

    await state.clear()


@router.callback_query(CallbackDataStartsWith('slots'))
async def slots_menu(call: CallbackQuery, _):
    val, user_id_str = call.data.split(":")
    user_id = int(user_id_str)

    if call.from_user.id != user_id:
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    chat_id = call.message.chat.id
    if not await db.is_game_enabled(chat_id, "slots"): # если как то тут оказались то нужно тоже блокировать
        await call.message.answer(_("slots_disabled"))
        return

    await call.message.delete()
    await call.message.answer_photo(
        photo='https://postimg.cc/bd3Y0KGX',
        caption=_("slots_menu_caption"),
        reply_markup=slots_kb(call.from_user.id, _)
    )