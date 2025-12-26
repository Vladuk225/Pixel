from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from utils.transform import transform_int
from utils.greetings import get_greeting
from database.user import User
from utils.filters.is_registered import IsRegisteredFilter
from utils.random_info_phrases import get_wallet_phrase
from keyboards.info import info_kb
from keyboards.options import options_kb
from utils.unauthorized_messages import get_random_unauthorized_message
from middlewares.i18n import I18nMiddleware
from utils.filters.text_in import TextIn
from aiogram.fsm.context import FSMContext


i18n_middleware = I18nMiddleware() 
router = Router()


@router.message(TextIn([
    'я', 
    'i'
]))
async def get_info(message: Message, _):
    if not IsRegisteredFilter():
        await message.answer(
            _("not_register_message")
        )
        return
    user = await User.get(message.from_user.id)
    await message.answer_photo(
        photo='https://postimg.cc/mzWXK9GZ',
        caption=f"{get_greeting(_)} {user.nickname}.\n{get_wallet_phrase(transform_int(user.balance), _)}",
        reply_markup=info_kb(message.from_user.id, _)
    )


@router.callback_query(F.data.startswith('options'))
async def menu_options(call: CallbackQuery, _):
    lol, user_id_str = call.data.split(":")
    if not call.from_user.id == int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    await call.message.delete()
    await call.message.answer(_("options_menu"), reply_markup=options_kb(call.from_user.id, _))


@router.callback_query(F.data.startswith('back_to_info'))
async def back_to_info_call(call: CallbackQuery, _):
    lol, user_id_str = call.data.split(":")
    if not call.from_user.id == int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    await call.message.delete()
    user = await User.get(call.from_user.id)
    await call.message.answer_photo(
        photo='https://postimg.cc/mzWXK9GZ',
        caption=f"{get_greeting(_)} {user.nickname}.\n{get_wallet_phrase(transform_int(user.balance), _)}",
        reply_markup=info_kb(call.from_user.id, _)
    )


@router.message(TextIn(
    ['отмена', 'cancel']
))
async def cancel(message: Message, state: FSMContext, _):
    if state:
        await state.clear()
    await message.answer(_("cancel_succesful"))