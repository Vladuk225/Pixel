from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from utils.filters.startswith import CallbackDataStartsWith
from utils.filters.text_in import TextIn
from keyboards.faq import faq_kb, back_to_faq_menu_kb
from keyboards.support import finish_report_kb
from aiogram.fsm.context import FSMContext
from states.support import SupportState
from utils.unauthorized_messages import get_random_unauthorized_message
from bot import bot
from config import admin_ids, ru_doc_link, en_doc_link
from database.user import User, Stats
from aiogram.filters import StateFilter
from database.rules import RulesDB
from database.links import LinksDB
from middlewares.i18n import I18nMiddleware
from database.lang import UserLanguageDB


router = Router()
rules = RulesDB()
links_db = LinksDB()
i18n_middleware = I18nMiddleware()
lang = UserLanguageDB()


@router.callback_query(CallbackDataStartsWith('faq'))
async def faq_menu(call: CallbackQuery, _):
    val, user_id_str = call.data.split(":")
    if not call.from_user.id == int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    await call.message.delete()
    await call.message.answer_photo(photo='https://postimg.cc/ThRYDR3y', caption=_("faq_menu_text"), reply_markup=faq_kb(call.from_user.id, _))


@router.message(TextIn([
    'информация', 
    'info'
]))
async def faq_menu(message: Message, _):
    await message.answer_photo(photo='https://postimg.cc/ThRYDR3y', caption=_("faq_menu_text"), reply_markup=faq_kb(message.from_user.id))


@router.message(StateFilter(SupportState.collecting_messages))
async def collect_support_messages(message: Message, state: FSMContext):
    data = await state.get_data()
    messages = data.get('messages', [])
    messages.append(message)
    await state.update_data(messages=messages)


@router.callback_query(
    StateFilter(SupportState.collecting_messages),
    F.data.startswith("support_finish")
)
async def finish_support_session(call: CallbackQuery, state: FSMContext, _):
    val, user_id_str = call.data.split(":")
    if not call.from_user.id == int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    user_id = call.from_user.id
    name = await User.get(user_id)
    name = name.nickname
    name = f'<a href="tg://user?id={user_id}">{name}</a>'

    data = await state.get_data()
    messages = data.get('messages', [])

    if not messages:
        return

    await call.message.edit_text(_("succes_message_report"), reply_markup=back_to_faq_menu_kb(user_id, _))

    for dev_id in admin_ids:
        try:
            await bot.get_chat(dev_id)

            await bot.send_message(dev_id, f'👤 Новое обращение от {name} (ID: {user_id})')
            for msg in messages:
                if msg.content_type == 'text':
                    await bot.send_message(dev_id, f'{msg.text}')
                elif msg.content_type == 'photo':
                    await bot.send_photo(dev_id, msg.photo[-1].file_id, caption=msg.caption or "")
                elif msg.content_type == 'document':
                    await bot.send_document(dev_id, msg.document.file_id, caption=msg.caption or "")
                elif msg.content_type == 'video':
                    await bot.send_video(dev_id, msg.video.file_id, caption=msg.caption or "")
                elif msg.content_type == 'audio':
                    await bot.send_audio(dev_id, msg.audio.file_id, caption=msg.caption or "")
                elif msg.content_type == 'voice':
                    await bot.send_voice(dev_id, msg.voice.file_id, caption=msg.caption or "")
                elif msg.content_type == 'sticker':
                    await bot.send_sticker(dev_id, msg.sticker.file_id)
                elif msg.content_type == 'animation':
                    await bot.send_animation(dev_id, msg.animation.file_id, caption=msg.caption or "")
                elif msg.content_type == 'video_note':
                    await bot.send_video_note(dev_id, msg.video_note.file_id)
                elif msg.content_type == 'contact':
                    contact = msg.contact
                    contact_text = f"📱 Контакт: {contact.first_name} {contact.last_name or ''}\n📞 Телефон: {contact.phone_number}\n👤 User ID: {contact.user_id or 'Не указан'}"
                    await bot.send_message(dev_id, contact_text)
                elif msg.content_type == 'location':
                    location = msg.location
                    await bot.send_location(dev_id, location.latitude, location.longitude)
                    await bot.send_message(dev_id, "📍 Геолокация отправлена")
                elif msg.content_type == 'venue':
                    venue = msg.venue
                    await bot.send_venue(dev_id, latitude=venue.location.latitude, longitude=venue.location.longitude, 
                                        title=venue.title, address=venue.address, 
                                        foursquare_id=venue.foursquare_id)
                elif msg.content_type == 'poll':
                    poll = msg.poll
                    await bot.send_poll(dev_id, question=poll.question, options=[o.text for o in poll.options], is_anonymous=poll.is_anonymous)
                elif msg.content_type == 'dice':
                    await bot.send_dice(dev_id, emoji=msg.dice.emoji)
            await bot.send_message(dev_id, '📩 Обращение завершено.')
        except Exception as e:
            print(f"Ошибка отправки сообщения админу {dev_id}: {e}")

    await state.clear()


@router.callback_query(CallbackDataStartsWith('support'))
async def faq_menu(call: CallbackQuery, state: FSMContext, _):
    val, user_id_str = call.data.split(":")
    if not call.from_user.id == int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    await call.message.delete()
    await state.update_data(messages=[])
    await call.message.answer(_("report_menu"), reply_markup=finish_report_kb(call.from_user.id, _))

    await state.set_state(SupportState.collecting_messages)


@router.callback_query(CallbackDataStartsWith('stats'))
async def rules_menu(call: CallbackQuery, _):
    val, user_id_str = call.data.split(":")
    if not call.from_user.id == int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    await call.message.delete()
    await call.message.answer_photo(photo='https://postimg.cc/vD387p1d', caption=_("stats_info_text").format(await Stats.total_users(), await Stats.total_chats(), await Stats.banned_users(), await Stats.count_active_users_24h()), reply_markup=back_to_faq_menu_kb(call.from_user.id, _))


@router.callback_query(CallbackDataStartsWith('rules'))
async def stats_info(call: CallbackQuery, _):
    val, user_id_str = call.data.split(":")
    if not call.from_user.id == int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    await call.message.delete()
    rules_text = await rules.get_rule()
    if not rules:
        rules_text = f'👤 {_("rules_not_found")}'
    await call.message.answer_photo(photo='https://postimg.cc/MXWKQWp3', caption=f'''
{_("rules_menu")}
                                    
{rules_text}
    ''', reply_markup=back_to_faq_menu_kb(call.from_user.id, _))


@router.callback_query(CallbackDataStartsWith('links'))
async def show_link(call: CallbackQuery, _):
    val, user_id_str = call.data.split(":")
    if not call.from_user.id == int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    await call.message.delete()
    link_text = await links_db.get_link()
    if not link_text:
        link_text = f'👤 {_("links_not_found_text")}'
    await call.message.answer_photo(
        photo='https://postimg.cc/H8sYDtNd',
        caption=f'''
{_("links_menu")}

{link_text}
        ''',
        reply_markup=back_to_faq_menu_kb(call.from_user.id, _)
    )


@router.callback_query(CallbackDataStartsWith('info'))
async def info_menu(call: CallbackQuery, _):
    val, user_id_str = call.data.split(":")
    if not call.from_user.id == int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    await call.message.delete()
    user_lang = await lang.get_language(call.from_user.id)
    await call.message.answer_photo(photo=_("doc_photo"), caption=_("doc_info").format(_('')), reply_markup=back_to_faq_menu_kb(call.from_user.id, _))