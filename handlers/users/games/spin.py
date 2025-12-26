from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from utils.unauthorized_messages import get_random_unauthorized_message
from keyboards.casino import spin_kb, spin_play_kb, spin_result_kb
import random
from aiogram.fsm.context import FSMContext
from states.casino import SpinGame
from database.user import User
from handlers.users.games.main import game_check
from utils.transform import transform_int
from utils.emojis import random_lose_emojis
from database.game_settings import GameSettingsDB
from utils.filters.startswith import CallbackDataStartsWith
import asyncio
from middlewares.i18n import I18nMiddleware


router = Router()
db = GameSettingsDB()
i18n_middleware = I18nMiddleware()


@router.callback_query(CallbackDataStartsWith('spin_play'))
async def spin_game(call: CallbackQuery, state: FSMContext, _):
    val, user_id_str = call.data.split(":")
    user_id = int(user_id_str)

    if call.from_user.id != user_id:
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    chat_id = call.message.chat.id
    if not await db.is_game_enabled(chat_id, "spin"):
        await call.message.answer(_("spin_disabled"))
        return
    await state.set_state(SpinGame.waiting_for_bet)
    await call.message.delete()
    await call.message.answer(_("spin_enter_bet"))


@router.message(SpinGame.waiting_for_bet)
async def process_spin_bet(msg: Message, state: FSMContext, _):
    bet = await game_check(msg, msg.text, _)
    if not bet:
        return
    await state.update_data(bet=bet)
    await state.set_state(SpinGame.waiting_for_play)
    await msg.answer(_("spin_bet_placed").format(bet=transform_int(bet)),
                     reply_markup=spin_play_kb(msg.from_user.id, _),
                     parse_mode="HTML")
    

@router.callback_query(F.data.startswith("spin_start"))
async def start_spin_game(call: CallbackQuery, state: FSMContext, _):
    val, user_id_str = call.data.split(":")
    user_id = int(user_id_str)

    if call.from_user.id != user_id:
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)

    data = await state.get_data()
    bet = data["bet"]
    await call.message.delete()

    all_emojis = ['🎰', '🍓', '🍒', '💎', '🍋', '🌕', '🖕', '💰', '🍎', '🎁', '💎', '💩', '🍩', '🍗', '🍏', '🔥', '🍊']
    emojis = [random.choice(all_emojis) for _ in range(3)]
    emj = '|{}|{}|{}|'.format(*emojis)

    multiplier = 0
    if len(set(emojis)) == 1:
        multiplier = 5
    else:
        for emoji in emojis:
            if emoji in ['💎', '🍋']:
                multiplier += 0.25
            elif emoji == '🎰':
                multiplier += 1

    payout = bet * multiplier
    user = await User.get(user_id_str)

    if payout != 0:
        multiplier += 1
        await call.message.answer(_(
            "spin_win",
        ).format(emj=emj, multiplier=multiplier, payout=transform_int(payout)), reply_markup=spin_result_kb(user_id_str, _))
        await user.add_balance(payout)
    else:
        await call.message.answer(_("spin_lose").format(emj=emj, bet=transform_int(bet)), 
        reply_markup=spin_result_kb(user_id_str, _))
        await user.subtract_balance(bet)

    await state.clear()


@router.callback_query(CallbackDataStartsWith('spin'))
async def spin_menu(call: CallbackQuery, _):
    val, user_id_str = call.data.split(":")
    user_id = int(user_id_str)

    if call.from_user.id != user_id:
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    chat_id = call.message.chat.id
    if not await db.is_game_enabled(chat_id, "spin"):
        await call.message.answer(_("spin_disabled"))
        return

    await call.message.delete()
    await call.message.answer_photo(
        photo='https://postimg.cc/5jn95ZXk',
        caption=_("spin_description"),
        reply_markup=spin_kb(call.from_user.id, _)
    )