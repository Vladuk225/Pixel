from aiogram import Router
from aiogram.types import Message, CallbackQuery
from utils.unauthorized_messages import get_random_unauthorized_message
from keyboards.jobs import jobs_kb 
from utils.filters.startswith import CallbackDataStartsWith
from utils.filters.text_in import TextIn
from middlewares.i18n import I18nMiddleware


router = Router()
i18n_middleware = I18nMiddleware()


async def send_menu_jobs(message, user_id, _):
    await message.answer_photo(photo='https://postimg.cc/JtP739s2', 
    caption=_("jobs_menu_text"), reply_markup=jobs_kb(user_id, _))


@router.callback_query(CallbackDataStartsWith('jobs'))
async def call_menu_jobs(call: CallbackQuery, _):
    val, user_id_str = call.data.split(":")
    if call.from_user.id != int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    await call.message.delete()
    await send_menu_jobs(call.message, call.from_user.id, _)


@router.message(TextIn([
    'работы', 
    'jobs'
]))
async def cmd_menu_jobs(message: Message, _):
    await send_menu_jobs(message, message.from_user.id, _)