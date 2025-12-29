from aiogram import Router
from database.user import User, NotificationSettings
from utils.filters.startswith import TextStartsWith
from aiogram.types import Message
from handlers.users.games.main import get_summ
from utils.transform import transform_int
from utils.emojis import random_win_emojis
from bot import bot
from config import admin_ids


router = Router()


@router.message(TextStartsWith('дать'))
async def give_money_cmd(message: Message, _):
    user_id = message.from_user.id

    try:
        reply_user_id = message.reply_to_message.from_user.id
    except AttributeError:
        return

    if user_id == reply_user_id:
        return
    balance = await User.get(user_id)
    balance = balance.balance
    try:
        summ = get_summ(message.text.split()[1], balance)
    except (ValueError, TypeError, IndexError):
        return
    comment = " ".join(message.text.split()[2:]) if len(message.text.split()) > 2 else ''
    user = await User.get(user_id)
    reply_user = await User.get(reply_user_id)
    reply_name = reply_user.nickname
    notifications = await NotificationSettings.get(user_id)
    if summ > 0:
        if balance >= summ:
            await message.answer(
                _("transfer_success").format(
                    status=await random_win_emojis(),
                    amount=transform_int(summ),
                    user=reply_name,
                    comment=comment
                )
            )
            if notifications.allow_transfers:
                await bot.send_message(
                    reply_user_id,
                    _("received_money").format(
                        user=reply_name,
                        amount=transform_int(summ)
                    )
                )
            if user_id not in admin_ids: 
                await user.subtract_balance(summ)
            await reply_user.add_balance(summ)
        else:
            await message.answer(_("insufficient_funds"))
            return
    else:
        return


@router.message(TextStartsWith('передать'))
async def transfer_money_cmd(message: Message, _):
    user_id = message.from_user.id
    parts = message.text.split()

    if len(parts) < 3:
        return

    try:
        target_user_id = int(parts[1])
    except ValueError:
        return 

    if user_id == target_user_id:
        return  

    balance = await User.get(user_id)
    balance = balance.balance

    try:
        summ = get_summ(parts[2], balance)
    except (ValueError, TypeError):
        return

    comment = " ".join(parts[3:]) if len(parts) > 3 else ''
    user = await User.get(user_id)
    reply_user = await User.get(target_user_id)
    reply_name = reply_user.nickname
    notifications = await NotificationSettings.get(target_user_id)

    if summ > 0:
        if balance >= summ:
            await message.answer(
                _("transfer_success").format(
                    status=await random_win_emojis(),
                    amount=transform_int(summ),
                    user=reply_name,
                    comment=comment
                )
            )
            if notifications.allow_transfers:
                await bot.send_message(
                    target_user_id,
                    _("received_money").format(
                        user=reply_name,
                        amount=transform_int(summ)
                    )
                )
            if user_id not in admin_ids:
                await user.subtract_balance(summ)
            await reply_user.add_balance(summ)
        else:
            await message.answer(_("insufficient_funds"))