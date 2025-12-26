from aiogram import Router
from aiogram.types import Message, CallbackQuery
from utils.filters.startswith import TextStartsWith, CallbackDataStartsWith
from keyboards.bonus import create_bonus_keyboard, bonus_claimed_kb
from database.bonus import BonusDB
import time
import random


router = Router()
db = BonusDB("database.db")


@router.callback_query(CallbackDataStartsWith('bonus_menu'))
async def bonus_menu(call: CallbackQuery, _):
    await db.ensure_user(call.from_user.id)
    user = await db.get_user(call.from_user.id)
    await call.message.delete()
    await call.message.answer(_("choose_bonus"), reply_markup=await create_bonus_keyboard(call.from_user.id, user, _))


@router.callback_query(CallbackDataStartsWith('bonus_'))
async def handle_bonus(call: CallbackQuery, _):
    try:
        data, uid_str = call.data.split(":")
        bonus_num = int(data.split("_")[1])
        user_id = int(uid_str)
    except:
        await call.answer(_("invalid_data"), show_alert=True)
        return

    await db.ensure_user(user_id)
    user = await db.get_user(user_id)

    if bonus_num == 2 and user.get("has_b2", 0) != 1:
        await call.answer(_("no_bonus_2"), show_alert=True)
        return
    if bonus_num == 3 and user.get("has_b3", 0) != 1:
        await call.answer(_("no_bonus_3"), show_alert=True)
        return

    now = int(time.time())
    last = user.get(f"b{bonus_num}_last_at") or 0
    BONUS_INTERVAL = 86400
    BONUS_AMOUNTS = {
        1: (50, 100),
        2: (200, 400),
        3: (800, 1500)
    }
    if now - last < BONUS_INTERVAL:
        remaining = BONUS_INTERVAL - (now - last)
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60
        await call.answer(
            _("bonus_wait_time").format(hours=hours, minutes=minutes),
            show_alert=True
        )
        return

    amount = random.randint(*BONUS_AMOUNTS[bonus_num])
    await db.record_bonus(user_id, bonus_num, amount)

    user = await db.get_user(user_id)
    await call.message.delete()
    await call.message.answer(
        _("bonus_received").format(bonus_num=bonus_num, amount=amount),
        reply_markup=await bonus_claimed_kb(user_id, _)
    )