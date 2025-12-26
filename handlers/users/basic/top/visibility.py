from aiogram import Router
from aiogram.types import Message
from database.user import TopVisibilityManager, User
from utils.filters.text_in import TextIn
from utils.emojis import random_lose_emojis, random_win_emojis
from decorators.admin_only import admin_only
from config import admin_ids


router = Router()


@router.message(TextIn([
    'топ спрятать',
    'top hide'
]))
async def cmd_hide_user(message: Message, _):
    user_id = message.from_user.id
    args = message.text.split()

    if user_id not in admin_ids:
        telegram_id = user_id
    else:
        if len(args) < 3 or not args[2].isdigit():
            return await message.answer(f"{await random_lose_emojis()} {_('specify_id_hide')}")
        telegram_id = int(args[2])

    await TopVisibilityManager.hide_user(telegram_id)
    user = await User.get(telegram_id)
    name = f'<a href="tg://user?id={telegram_id}">{user.nickname}</a>'
    await message.answer(_('user_hidden').format(name=name))


@router.message(TextIn([
    'топ показать',
    'top show'
]))
async def cmd_unhide_user(message: Message, _):
    user_id = message.from_user.id
    args = message.text.split()

    if user_id not in admin_ids:
        telegram_id = user_id
    else:
        if len(args) < 3 or not args[2].isdigit():
            return await message.answer(f"{await random_lose_emojis()} {_('specify_id_show')}")
        telegram_id = int(args[2])

    await TopVisibilityManager.unhide_user(telegram_id)
    user = await User.get(telegram_id)
    name = f'<a href="tg://user?id={telegram_id}">{user.nickname}</a>'
    await message.answer(_('user_shown').format(name=name))


@router.message(TextIn([
    'топ статус',
    'top status'
]))
async def cmd_is_hidden(message: Message, _):
    user_id = message.from_user.id
    args = message.text.split()

    if user_id not in admin_ids:
        telegram_id = user_id
    else:
        if len(args) < 3 or not args[2].isdigit():
            return await message.answer(f"{await random_lose_emojis()} {_('specify_id_status')}")
        telegram_id = int(args[2])

    user = await User.get(telegram_id)
    name = f'<a href="tg://user?id={telegram_id}">{user.nickname}</a>'
    if await TopVisibilityManager.is_hidden(telegram_id):
        await message.answer(f"{await random_win_emojis()} {_('user_is_hidden').format(name=name)}")
    else:
        await message.answer(f"{await random_lose_emojis()} {_('user_is_visible').format(name=name)}")


@router.message(TextIn([
    'топ спрятанные',
    'top hidden'
]))
@admin_only
async def cmd_hidden_list(message: Message, _):
    text = await TopVisibilityManager.format_hidden_users(_)
    await message.answer(text, parse_mode="HTML")