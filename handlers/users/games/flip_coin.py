from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from utils.unauthorized_messages import get_random_unauthorized_message
from keyboards.casino import flip_coin_kb, coin_choice_kb, coin_play_kb, coin_result_kb, choose_player_kb, pvp_invite_kb, coin_side_kb
import random
from aiogram.fsm.context import FSMContext
from states.casino import CoinGame
from database.user import User
from handlers.users.games.main import game_check
from utils.transform import transform_int
from utils.emojis import random_lose_emojis
# from database.coin_game import CoinPVPGame
from database.game_settings import GameSettingsDB
from middlewares.i18n import I18nMiddleware


router = Router()
pvp_requests = {}
# game_db = CoinPVPGame()
db = GameSettingsDB()
i18n_middleware = I18nMiddleware()


@router.callback_query(F.data.startswith("flip_coin_with_player"))
async def start_pvp_coin_game_callback(call: CallbackQuery, _):
    await call.message.answer(_("coin_coming_soon"))
#     if call.message.chat.type != "private":
#         await call.message.answer(f"{random_lose_emojis()} Играть с игроками в монетку можно только в личных сообщениях бота")
#         return
#     await state.set_state(CoinGame.waiting_for_opponent)
#     await call.message.delete()

#     await call.message.answer(
#         "👥 Выбери игрока, с которым хочешь сыграть в монетку:",
#         reply_markup=choose_player_kb()
#     )


# @router.message(CoinGame.waiting_for_opponent, F.user_shared)
# async def handle_user_choice(msg: Message, state: FSMContext):
#     opponent_id = msg.user_shared.user_id
#     initiator_id = msg.from_user.id
#     if opponent_id == initiator_id:
#         return await msg.answer("❗ Ты не можешь играть сам с собой.")

#     game_id = game_db.create_game(initiator_id, opponent_id)
#     await state.update_data(game_id=game_id, initiator_id=initiator_id, opponent_id=opponent_id)
#     await state.set_state(CoinGame.waiting_for_pvp_bet)
#     await msg.answer("💰 Введи сумму ставки:")


# @router.message(CoinGame.waiting_for_pvp_bet)
# async def handle_bet_input(msg: Message, state: FSMContext):
#     bet = await game_check(msg, msg.text)
#     if not bet:
#         return

#     data = await state.get_data()
#     game_id = data["game_id"]
#     print(game_id)
#     game_db.set_bet(game_id, bet)

#     await state.set_state(CoinGame.waiting_for_opponent_response)
#     opponent_id = data["opponent_id"]
#     initiator_id = data["initiator_id"]

#     await msg.answer("📨 Запрос отправлен игроку!")
#     await msg.bot.send_message(
#         chat_id=opponent_id,
#         text=(
#             f"🎮 Игрок <a href='tg://user?id={initiator_id}'>вызвал тебя</a> на игру в монетку!\n"
#             f"💰 Ставка: <b>{bet}</b> монет\n\nПринять вызов?"
#         ),
#         reply_markup=pvp_invite_kb(initiator_id),
#         parse_mode="HTML"
#     )


# @router.callback_query(F.data.startswith("coin_pvp_accept"))
# async def accept_pvp_game(call: CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     game_id = data.get("game_id")
#     initiator_id = data.get("initiator_id")
#     opponent_id = call.from_user.id

#     # if not game_db.get_game(game_id):
#     #     return await call.answer("❗ Игра не найдена или уже завершена.", show_alert=True)

#     await call.message.edit_text("✅ Ты принял вызов! Скоро начнётся игра!")
#     await call.bot.send_message(
#         chat_id=initiator_id,
#         text=f"🎮 Игрок <a href='tg://user?id={opponent_id}'>принял</a> твой вызов! 🎉\n\nВыберите стороны: орёл или решка.",
#         parse_mode="HTML"
#     )

#     for user_id in (initiator_id, opponent_id):
#         await call.bot.send_message(
#             chat_id=user_id,
#             text="Выбери сторону монеты:",
#             reply_markup=coin_choice_kb(user_id)
#         )

#     await state.set_state(CoinGame.waiting_for_pvp_choice)


# @router.callback_query(F.data.startswith("coin_choice"))
# async def handle_coin_choice(call: CallbackQuery, state: FSMContext):
#     _, choice, user_id_str = call.data.split(":")
#     user_id = int(user_id_str)

#     if call.from_user.id != user_id:
#         return await call.answer(get_random_unauthorized_message(), show_alert=True)

#     data = await state.get_data()
#     game_id = data.get("game_id")
#     initiator_id = data.get("initiator_id")
#     opponent_id = data.get("opponent_id")

#     game_db.set_choice(game_id, user_id, choice)
#     await call.message.edit_text(f"✅ Ты выбрал {'орёл' if choice == 'heads' else 'решка'}.")

#     if game_db.both_choices_made(game_id):
#         game = game_db.get_game(game_id)
#         initiator_choice = game[4]  
#         opponent_choice = game[5]   
#         bet = game[3]        

#         result = random.choice(["heads", "tails"])
#         game_db.set_result(game_id, result)
#         emoji = "🦅" if result == "heads" else "💠"

#         winner_id = None
#         if initiator_choice == result and opponent_choice != result:
#             winner_id = initiator_id
#             loser_id = opponent_id
#         elif opponent_choice == result and initiator_choice != result:
#             winner_id = opponent_id
#             loser_id = initiator_id

#         if winner_id:
#             await call.bot.send_message(winner_id,
#                 f"{emoji} Выпал {'орёл' if result == 'heads' else 'решка'}!\n\n🎉 Ты победил и получаешь {bet * 2} монет!"
#             )
#             await call.bot.send_message(loser_id,
#                 f"{emoji} Выпал {'орёл' if result == 'heads' else 'решка'}!\n\n💸 Ты проиграл."
#             )
#         else:
#             await call.bot.send_message(initiator_id,
#                 f"{emoji} Выпал {'орёл' if result == 'heads' else 'решка'}!\n🤝 Ничья!"
#             )
#             await call.bot.send_message(opponent_id,
#                 f"{emoji} Выпал {'орёл' if result == 'heads' else 'решка'}!\n🤝 Ничья!"
#             )

#         await state.clear()


# @router.callback_query(F.data.startswith("coin_pvp_decline"))
# async def decline_pvp_game(call: CallbackQuery):
#     initiator_id = int(call.data.split(":")[1])
#     opponent_id = call.from_user.id

#     if pvp_requests.get(opponent_id) == initiator_id:
#         del pvp_requests[opponent_id]

#     await call.message.edit_text("❌ Ты отклонил вызов.")
#     await call.bot.send_message(
#         chat_id=initiator_id,
#         text=f"🚫 Игрок <a href='tg://user?id={opponent_id}'>отклонил</a> твой вызов.",
#         parse_mode="HTML"
#     )


@router.callback_query(F.data.startswith("flip_coin_with_bot"))
async def flip_coin_with_bot(call: CallbackQuery, state: FSMContext, _):
    val, user_id_str = call.data.split(":")
    user_id = int(user_id_str)

    if call.from_user.id != user_id:
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)

    chat_id = call.message.chat.id
    if not await db.is_game_enabled(chat_id, "coin"):
        await call.message.answer(_("coin_unabled_in_chat"))
        return

    await state.set_state(CoinGame.waiting_for_bet)
    await call.message.delete()
    await call.message.answer(_("choose_bet_coin"))


@router.callback_query(F.data.startswith('flip_coin'))
async def flip_coin_menu(call: CallbackQuery, _):
    val, user_id_str = call.data.split(":")
    user_id = int(user_id_str)

    if call.from_user.id != user_id:
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)

    chat_id = call.message.chat.id
    if not await db.is_game_enabled(chat_id, "coin"):
        await call.message.answer(_("coin_unabled_in_chat"))
        return

    await call.message.delete()
    await call.message.answer_photo(
        photo='https://postimg.cc/c6s4nsLr',
        caption=_("coin_menu"),
        reply_markup=flip_coin_kb(call.from_user.id, _)
    )


@router.message(CoinGame.waiting_for_bet)
async def process_coin_bet(msg: Message, state: FSMContext, _):
    bet = await game_check(msg, msg.text, _)
    if not bet:
        return
    await state.update_data(bet=bet)
    await state.set_state(CoinGame.waiting_for_play)
    await msg.answer(_("coin_menu"),
        reply_markup=coin_play_kb(msg.from_user.id, _),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("coin_start"))
async def start_coin_game(call: CallbackQuery, state: FSMContext, _):
    val, user_id_str = call.data.split(":")
    if call.from_user.id != int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)

    await state.set_state(CoinGame.waiting_for_choice)  
    await call.message.edit_text(
        _("choose_side_coin"),
        reply_markup=coin_choice_kb(call.from_user.id, _)
    )


@router.callback_query(F.data.startswith("coin_choice"))
async def process_coin_choice(call: CallbackQuery, state: FSMContext, _):
    val, choice, user_id_str = call.data.split(":")
    user_id = int(user_id_str)

    if call.from_user.id != user_id:
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)

    stored_data = await state.get_data()
    bet = stored_data.get("bet", 0)
    user = await User.get(user_id)
    user_choice = _("coin_heads") if choice == "head" else _("coin_tails")

    roll = random.randint(1, 100)
    if roll <= 2:
        result = "edge"
    else:
        result = random.choice(["head", "tail"])

    await state.clear()
    await call.message.delete()

    if result == "edge":
        text = (
            _("coin_edge_message")
            .replace('[user_choice]', user_choice)
            .replace('[bet]', transform_int(bet))
        )
    elif choice == result:
        await user.add_balance(bet * 2)
        result_text = _("coin_heads") if result == "head" else _("coin_tails")
        text = (
            _("coin_win_message")
            .replace('[user_choice]', user_choice)
            .replace('[result_text]', result_text)
            .replace('[bet]', transform_int(bet * 2))
        )
    else:
        await user.subtract_balance(bet)
        result_text = _("coin_heads") if result == "head" else _("coin_tails")
        text = (
            _("coin_lose_message")
            .replace('[user_choice]', user_choice)
            .replace('[result_text]', result_text)
            .replace('[bet]', transform_int(bet))
        )
    await call.message.answer(
        text,
        reply_markup=coin_result_kb(call.from_user.id, _),
        parse_mode="HTML"
    )