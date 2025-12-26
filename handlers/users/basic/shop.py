from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from utils.filters.startswith import TextStartsWith, CallbackDataStartsWith
from utils.unauthorized_messages import get_random_unauthorized_message
from middlewares.i18n import I18nMiddleware
from keyboards.shop import shop_kb


router = Router()
i18n_middleware = I18nMiddleware()


@router.callback_query(F.data.startswith("shop"))
async def shop_menu(call: CallbackQuery, _):
    val, user_id_str = call.data.split(":")
    if not call.from_user.id == int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    await call.message.delete()
    await call.message.answer(text=_("shop_btn_text"), reply_markup=shop_kb(call.from_user.id, _))


@router.callback_query(F.data.startswith("bonus"))
async def shop_menu(call: CallbackQuery, _):
    val, user_id_str = call.data.split(":")
    if not call.from_user.id == int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    await call.message.delete()
    await call.message.answer(text=_("shop"), reply_markup=shop_kb(call.from_user.id, _))