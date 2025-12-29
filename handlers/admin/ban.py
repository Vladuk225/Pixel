from aiogram import Router, F
from aiogram.types import Message
from database.user import BanDatabase, User
import time
import re
from utils.emojis import random_win_emojis, random_lose_emojis
from utils.filters.startswith import TextStartsWith
from config import owner_id
from decorators.admin_only import admin_only
from utils.filters.text_in import TextIn


router = Router()


def parse_duration(duration_str: str) -> int:
    match = re.fullmatch(r"(\d+)([мmчhдd])", duration_str.lower())
    if not match:
        return 0
    num, unit = int(match[1]), match[2]
    return num * {"м": 60, "m": 60, "ч": 3600, "h": 3600, "д": 86400, "d": 86400}[unit]


@router.message(TextIn([
    'бан', 
    'ban'
]))
@admin_only
async def ban_command(message: Message, _):
    args = message.text.split(maxsplit=4)
    if len(args) < 4:
        return await message.answer(f"{await random_lose_emojis()} {_('ban_usage')}")
    try:
        user_id = int(args[1])
        if user_id == owner_id:
            return
        duration = parse_duration(args[2])
        if duration == 0:
            return await message.answer(f"{await random_lose_emojis()} {_('ban_incorrect_time')}")
        reason = args[3] if len(args) >= 4 else _('ban_no_reason')
        await BanDatabase.ban_user(user_id, reason, duration)
        name = await User.get(user_id)
        name = name.nickname
        name = f'<a href="tg://user?id={user_id}">{name}</a>'
        await message.answer(
            f"{await random_win_emojis()} {_('ban_success').format(name=name, time=args[2], reason=reason)}"
        )
    except Exception as e:
        await message.answer(f"{await random_lose_emojis()} {_('ban_error').format(error=e)}")


@router.message(TextIn([
    'разбан', 
    'unban'
]))
@admin_only
async def unban_command(message: Message, _):
    args = message.text.split()
    if len(args) != 2:
        return await message.answer(f"{await random_lose_emojis()} {_('unban_usage')}")
    try:
        user_id = int(args[1])
        await BanDatabase.unban_user(user_id)
        await message.answer(f"{await random_win_emojis()} {_('unban_success').format(user_id=user_id)}")
    except Exception as e:
        await message.answer(f"{await random_lose_emojis()} {_('ban_error').format(error=e)}")


@router.message(TextIn([
    'забаненные', 
    'banned'
]))
@admin_only
async def banned_list(message: Message, _):
    now = int(time.time())
    bans = await BanDatabase.get_all_bans()
    if not bans:
        return await message.answer(f"{await random_lose_emojis()} {_('banned_empty')}")
    text = _('banned_list_title')
    for user_id, reason, until in bans:
        remaining = until - now
        if remaining <= 0:
            continue 
        minutes = remaining // 60
        text += _('banned_list_item').format(user_id=user_id, minutes=minutes, reason=reason) + "\n"
    await message.answer(text or f"{await random_lose_emojis()} {_('banned_empty')}")