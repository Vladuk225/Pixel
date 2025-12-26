from aiogram import Router
from aiogram.types import CallbackQuery, Message
from utils.unauthorized_messages import get_random_unauthorized_message
from utils.filters.startswith import CallbackDataStartsWith, TextStartsWith
from middlewares.i18n import I18nMiddleware
from database.tiktok import ChannelDB
from aiogram.fsm.context import FSMContext
from states.tiktok import TikTokState, TikTokOptionsState
from keyboards.jobs import tik_tok_kb, back_to_tik_tok_menu_kb, confirm_delete_kb, back_to_jobs_menu_kb
from utils.emojis import random_win_emojis, random_lose_emojis
from bot import bot
import random
import time
from database.user import User


router = Router()
i18n_middleware = I18nMiddleware()


@router.callback_query(CallbackDataStartsWith('tik_tok_blogger'))
async def tik_tok_blogger_menu(call: CallbackQuery, state: FSMContext, _):
    val, user_id_str = call.data.split(":")
    if call.from_user.id != int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    tik_tok_id = await ChannelDB().get_channel_id(user_id_str)
    tik_tok_job = await ChannelDB().get_channel(tik_tok_id)
    if not tik_tok_job:
        await call.message.delete()
        await call.message.answer(_("tiktok_blogger_menu_register"))
        await state.set_state(TikTokState.nickname)
        return
    channel_id, channel_user_id, name, subscribers, likes, last_ad, last_video, last_like = tik_tok_job
    await call.message.delete()
    await call.message.answer_photo(photo='https://postimg.cc/JtP739s2', caption=_("tik_tok_info").format(name, subscribers, likes), reply_markup=tik_tok_kb(user_id_str, _))


@router.callback_query(CallbackDataStartsWith('tik_tok_video'))
async def tik_tok_make_video(call: CallbackQuery, _):
    val, user_id_str = call.data.split(":")
    user_id = int(user_id_str)

    if call.from_user.id != user_id:
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)

    channel_id = await ChannelDB.get_channel_id(user_id)
    channel = await ChannelDB.get_channel(channel_id)

    val1, val2, name, subscribers, likes, last_ad, last_video, last_like = channel

    now = int(time.time())

    if last_video and now - last_video < 300:
        remaining = 300 - (now - last_video)
        minutes, seconds = divmod(remaining, 60)
        return await call.answer(
            _("video_too_soon").format(minutes, seconds),
            show_alert=True
        )

    if random.choice([True, False]):
        change = random.randint(5, 50)
        action_text = f"{await random_win_emojis()} " + _("video_subscribed").format(change)
        await ChannelDB.update_subscribers(channel_id, max(0, change))
    else:
        change = random.randint(1, min(20, subscribers)) if subscribers > 0 else 0
        change = -change
        await ChannelDB.update_subscribers(channel_id, change)
        action_text = f"{await random_lose_emojis()} " + _("video_unsubscribed").format(abs(change))

    await call.message.delete()

    await call.message.answer(
        _("video_posted_followers").format(action_text),
        reply_markup=back_to_tik_tok_menu_kb(user_id, _)
    )


@router.callback_query(CallbackDataStartsWith('tik_tok_ad'))
async def tik_tok_make_ad(call: CallbackQuery, _):
    val, user_id_str = call.data.split(":")
    user_id = int(user_id_str)
    if call.from_user.id != user_id:
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    channel_id = await ChannelDB.get_channel_id(user_id)
    channel = await ChannelDB.get_channel(channel_id)
    val1, val2, name, subscribers, likes, last_ad, last_video, last_like = channel
    if subscribers < 300:
        return await call.answer(_("ad_not_enough_subs"), show_alert=True)
    now = int(time.time())
    cooldown = 5 * 60
    if last_ad and now - last_ad < cooldown:
        remaining = cooldown - (now - last_ad)
        mins, secs = divmod(remaining, 60)
        return await call.answer(_("ad_too_soon").format(mins, secs), show_alert=True)
    reward = random.randint(100, 500)
    user = await User.get(user_id)
    await user.add_balance(reward)
    action_text = f"{await random_win_emojis()} " + _("ad_earned").format(reward)
    await ChannelDB.update_last_ad(channel_id)
    await call.message.delete()
    await call.message.answer(
        _("ad_posted_money").format(action_text),
        reply_markup=back_to_tik_tok_menu_kb(user_id, _)
    )


@router.message(TextStartsWith('тикток лайк'))
async def tik_tok_like(message: Message, _):
    user_id = message.from_user.id
    try:
        user_id_reply = message.reply_to_message.from_user.id
        if user_id_reply == user_id:
            raise AttributeError
    except AttributeError:
        return
    channel_id = await ChannelDB.get_channel_id(user_id)
    reply_channel_id = await ChannelDB.get_channel_id(user_id_reply)
    channel = await ChannelDB.get_channel(channel_id)
    reply_channel = await ChannelDB.get_channel(reply_channel_id)
    val1, val2, name, subscribers, likes, last_ad, last_video, last_like = channel
    now = int(time.time())
    cooldown = 5 * 60
    if last_like and now - last_like < cooldown:
        remaining = cooldown - (now - last_like)
        mins, secs = divmod(remaining, 60)
        return await message.answer(_("like_too_soon").format(mins, secs), show_alert=True)
    try:
        val1, val2, name, subscribers, likes, last_ad, last_video, last_like = reply_channel
    except:
        await message.answer(f'{await random_lose_emojis()} {_("user_tiktok_status")}')
        return
    await ChannelDB.update_likes(reply_channel_id, user_id)
    await message.answer(_("like_success"))


@router.message(TikTokState.nickname)
async def process_tik_tok_channel_register(message: Message, state: FSMContext, _):
    user_id = message.from_user.id
    nickname = message.text
    await message.answer(_("tik_tok_registration_succes").replace('[name]', nickname))
    channel_id = await ChannelDB().add_channel(user_id, nickname)
    tik_tok_job = await ChannelDB().get_channel(channel_id)
    channel_id, channel_user_id, name, subscribers, likes, last_ad, last_video, last_like = tik_tok_job
    await message.answer_photo(photo='https://postimg.cc/JtP739s2', caption=_("tik_tok_info").format(name, subscribers, likes), reply_markup=tik_tok_kb(user_id, _))
    await state.clear()


@router.callback_query(CallbackDataStartsWith('tik_tok_change_name'))
async def tik_tok_change_name(call: CallbackQuery, state: FSMContext, _):
    val, user_id_str = call.data.split(":")
    if call.from_user.id != int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    await call.message.delete()
    msg = await call.message.answer(_("tik_tok_change_name_text"))
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(TikTokOptionsState.set_channel_name)


@router.message(TikTokOptionsState.set_channel_name)
async def process_tik_tok_set_channel_name(message: Message, state: FSMContext, _):
    name = message.text
    user_id = message.from_user.id
    data = await state.get_data()
    msg_id = data["msg_id"]
    await bot.delete_message(message.chat.id, msg_id)
    await message.answer(f'{await random_win_emojis()} {_("succes_tik_tok_change_name_text")}')
    channel_id = await ChannelDB().get_channel_id(user_id)
    await ChannelDB().update_channel_name(channel_id, name)
    await state.clear()


@router.callback_query(CallbackDataStartsWith('tik_tok_delete'))
async def tik_tok_delete_account(call: CallbackQuery, _):
    val, user_id_str = call.data.split(":")
    if call.from_user.id != int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)

    await call.message.delete()
    await call.message.answer(
        _("delete_confirmation"),
        reply_markup=confirm_delete_kb(int(user_id_str), _)
    )


@router.callback_query(CallbackDataStartsWith('tik_tok_confirm_delete'))
async def tik_tok_confirm_delete(call: CallbackQuery, _):
    val, action, user_id_str = call.data.split(":")
    user_id = int(user_id_str)

    if call.from_user.id != user_id:
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)

    await call.message.delete()

    if action == "yes":
        channel_id = await ChannelDB().get_channel_id(user_id)
        if channel_id:
            await ChannelDB().delete_channel(channel_id)
        await call.message.answer(
            _("account_deleted").format(emoji=await random_win_emojis()),
            reply_markup=back_to_jobs_menu_kb(user_id, _)
        )
    else:
        await call.message.answer(
            _("delete_cancelled").format(emoji=await random_lose_emojis()),
            reply_markup=back_to_jobs_menu_kb(user_id, _)
        )