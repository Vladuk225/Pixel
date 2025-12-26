from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.notifications import notifications_kb
from database.user import NotificationSettings
from utils.unauthorized_messages import get_random_unauthorized_message
from utils.filters.text_in import TextIn
from middlewares.i18n import I18nMiddleware


router = Router()
i18n_middleware = I18nMiddleware()


@router.callback_query(F.data.startswith('notifications'))
async def notifications_settings_call(call: CallbackQuery, _):
    val, user_id_str = call.data.split(":")
    if not call.from_user.id == int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    settings = await NotificationSettings.get(call.from_user.id)
    await call.message.delete()
    await call.message.answer(_("notifications_menu"), reply_markup=notifications_kb(settings.allow_transfers, call.from_user.id, _))


@router.message(TextIn([
    'уведомления',
    'notifications'
]))
async def notifications_settings(message: Message, _):
    settings = await NotificationSettings.get(message.from_user.id)
    await message.answer(_("notifications_menu"), reply_markup=notifications_kb(settings.allow_transfers, message.from_user.id, _))


@router.callback_query(F.data.startswith("toggle_transfers"))
async def toggle_transfers_callback(call: CallbackQuery, _):
    val, user_id_str = call.data.split(":")
    if not call.from_user.id == int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    telegram_id = call.from_user.id
    settings = await NotificationSettings.get(telegram_id)
    new_status = 0 if settings.allow_transfers else 1
    await settings.update_allow_transfers(new_status)

    await call.message.edit_text(_("notifications_menu"), reply_markup=notifications_kb(settings.allow_transfers, telegram_id, _))