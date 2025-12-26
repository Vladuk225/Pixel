from aiogram import Router
from aiogram.types import Message, CallbackQuery
from utils.filters.startswith import CallbackDataStartsWith
from database.user import Leaderboard
from utils.unauthorized_messages import get_random_unauthorized_message
from keyboards.top import top_kb
from utils.filters.text_in import TextIn
from middlewares.i18n import I18nMiddleware


i18n_middleware = I18nMiddleware()
router = Router()


@router.message(TextIn([
    'топ', 
    'top'
]))
async def top_command(message: Message, _):
    try:
        limit = int(message.text.split()[1])
    except:
        limit = 10
    text = await Leaderboard.format_top_users(limit, message.from_user.id, _)
    await message.answer(text, reply_markup=top_kb(message.from_user.id, _))


@router.callback_query(CallbackDataStartsWith('top'))
async def call_top_command(call: CallbackQuery, _: dict):
    val, user_id_str = call.data.split(":")
    if not call.from_user.id == int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    text = await Leaderboard.format_top_users(10, call.from_user.id, _)
    await call.message.delete()
    await call.message.answer(text, reply_markup=top_kb(call.from_user.id, _))