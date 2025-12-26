from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.lang import UserLanguageDB
from keyboards.language import get_language_keyboard
from utils.filters.startswith import CallbackDataStartsWith
from utils.unauthorized_messages import get_random_unauthorized_message
from middlewares.i18n import I18nMiddleware


router = Router()
db = UserLanguageDB()
i18n_middleware = I18nMiddleware()


@router.callback_query(CallbackDataStartsWith('language'))
async def language_menu(call: CallbackQuery, _):  
    huinia, user_id_str = call.data.split(":")
    if not call.from_user.id == int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    user_id = call.from_user.id
    current_lang = await db.get_language(user_id)
    await call.message.edit_text(
        _("choose_language"), 
        reply_markup=get_language_keyboard(current_lang, user_id, _)
    )


@router.callback_query(F.data.startswith("set_lang-"))
async def set_language_callback(callback: CallbackQuery, _):  
    huinia, user_id_str = callback.data.split(":")
    if not callback.from_user.id == int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(callback.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await callback.answer(msg, show_alert=True)
    user_id = callback.from_user.id
    lang_code = callback.data.split("-")[1]
    lang_code = lang_code.split(':')[0]
    await db.set_language(user_id, lang_code)
    await callback.message.edit_text(
        text=_("choose_language"),
        reply_markup=get_language_keyboard(lang_code, user_id, _)
    )