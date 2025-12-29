from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from utils.unauthorized_messages import get_random_unauthorized_message
from keyboards.casino import casino_kb, get_game_settings_keyboard
from database.user import User
from database.game_settings import GameSettingsDB
from utils.emojis import random_lose_emojis, random_win_emojis
from decorators.chat_admin_only import chat_admin_only
from middlewares.i18n import I18nMiddleware
from utils.filters.text_in import TextIn


i18n_middleware = I18nMiddleware()
router = Router()
db = GameSettingsDB()


def get_summ(summ, balance):
    summ = summ.lower().strip()  
    if summ in ['все', 'всё', "all"]:
        return balance
    if summ in ['половина', 'пол', 'half']:
        return balance // 2
    summ = summ.replace('е', 'e')
    summ = summ.replace('к', '000').replace('м', '000000').replace('k', '000').replace('m', '000000')
    return int(summ)


async def game_check(message, summ, _):
    balance = await User.get(message.from_user.id)
    balance = balance.balance
    try:
        summ = get_summ(summ, balance)
    except ValueError:
        await message.answer(f'{await random_lose_emojis()} {_("enter_valid_bet_amount")}')
        return None
    if summ > balance:
        await message.answer(f'{await random_lose_emojis()} {_("insufficient_funds")}')
        return None
    if summ < 10:
        await message.answer(f'{await random_lose_emojis()} {_("min_bet")}')
        return None    
    return summ
    

async def send_casino_menu(user_id: int, message, _):
    await message.answer_photo(
        photo='https://postimg.cc/c6s4nsLr',
        caption=_("casino_menu"),
        reply_markup=casino_kb(user_id, _)
    )


@router.callback_query(F.data.startswith('casino'))
async def menu_casino(call: CallbackQuery, _):
    val, user_id_str = call.data.split(":")
    user_id = int(user_id_str)

    if call.from_user.id != user_id:
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)

    await call.message.delete()
    await send_casino_menu(call.from_user.id, call.message, _)


@router.message(TextIn(['казино', 'casino']))
async def casino_command_handler(message: Message, _):
    await send_casino_menu(message.from_user.id, message, _)


@router.message(TextIn(['меню чата', 'chat menu']))
@chat_admin_only()
async def show_settings(message: Message, _):
    chat_id = message.chat.id
    statuses = await db.get_statuses(chat_id)
    keyboard = get_game_settings_keyboard(statuses, _)
    await message.answer(_("chat_game_settings"), reply_markup=keyboard)


@router.callback_query(F.data.startswith("game_toggle_"))
async def toggle_game(callback: CallbackQuery, _):
    val, user_id_str = callback.data.split(":")
    user_id = int(user_id_str)

    if callback.from_user.id != user_id:
        _caller = await i18n_middleware.get_localizer_for_user(callback.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await callback.answer(msg, show_alert=True)
    chat_id = callback.message.chat.id
    game_name = callback.data.replace("game_toggle_", "")
    new_status = await db.toggle_game(chat_id, game_name)

    if new_status is not None:
        statuses = await db.get_statuses(chat_id)
        keyboard = get_game_settings_keyboard(statuses)
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    else:
        await callback.answer(_("game_not_found"), show_alert=True)


@router.callback_query(F.data.startswith('back_to_menu_casino'))
async def menu_casino(call: CallbackQuery, _):
    val, user_id_str = call.data.split(":")
    user_id = int(user_id_str)

    if call.from_user.id != user_id:
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    await call.message.delete()
    await send_casino_menu(call.from_user.id, call.message, _)