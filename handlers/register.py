from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.registration import RegistrationState
from config import start_balance
from database.user import User
from keyboards.register import get_register_select_gender_keyboard
from keyboards.info import info_kb
from utils.transform import transform_int
from utils.greetings import get_greeting
from decorators.only_private_chat import private_chat_only
from utils.random_info_phrases import get_wallet_phrase
import asyncio
from utils.unauthorized_messages import get_random_unauthorized_message
from middlewares.i18n import I18nMiddleware


i18n_middleware = I18nMiddleware()
router = Router()


@router.callback_query(F.data.startswith('register_user'))
async def start_registration(call: CallbackQuery, state: FSMContext, _):
    val, user_id_str = call.data.split(":")
    user_id = int(user_id_str)

    if call.from_user.id != user_id:
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    await call.message.delete()
    await call.message.answer(_("choose_nickname"))
    await call.answer()
    await state.set_state(RegistrationState.enter_username)
    

@router.message(RegistrationState.enter_username)
async def process_registration_2(message: Message, state: FSMContext, _):
    nickname = message.text
    await state.update_data(nickname=nickname)
    await message.answer(_("choose_gender"), reply_markup=get_register_select_gender_keyboard(message.from_user.id, _))
    await state.set_state(RegistrationState.choose_gender)


@router.callback_query(F.data.startswith('gender_'))
async def process_finish_registration(call: CallbackQuery, state: FSMContext, _):
    val, user_id_str = call.data.split(":")
    user_id = int(user_id_str)

    if call.from_user.id != user_id:
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    await call.message.edit_text(_("process_register"))
    await asyncio.sleep(4)
    gender = call.data.split('_')[1]
    gender = gender.split(':')[0]
    data = await state.get_data()
    nickname = data.get("nickname")
    game_id = await User.generate_new_game_id()
    user = User(
        telegram_id=call.from_user.id,
        game_id=game_id,
        nickname=nickname,
        gender=gender,
        balance=start_balance
    )
    await user.save()
    gender = _("male_gender") if gender == 'male' else _("female_gender")
    successful_register_text = _("successful_register")
    successful_register_text = successful_register_text.replace('[nickname]', nickname).replace('[game_id]', str(game_id)).replace('[gender]', gender).replace('[balance]', transform_int(start_balance))
    await call.message.edit_text(successful_register_text)
    user = await User.get(call.from_user.id)
    await call.message.answer_photo(
        photo='https://postimg.cc/mzWXK9GZ',
        caption=f"{get_greeting(_)} {user.nickname}.\n{get_wallet_phrase(transform_int(user.balance), _)}",
        reply_markup=info_kb(call.from_user.id, _)
    )
    await state.clear()
    await call.answer()