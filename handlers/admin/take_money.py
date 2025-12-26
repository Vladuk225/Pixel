from aiogram import Router, F
from aiogram.types import Message
from database.user import User
from utils.transform import transform_int
from aiogram.exceptions import TelegramAPIError
from bot import bot
from database.user import NotificationSettings
from decorators.admin_only import admin_only
from utils.filters.text_in import TextIn


router = Router()


@router.message(TextIn([
    'забрать', 
    'take'
]))
@admin_only
async def take_money(message: Message, _):
    parts = message.text.split()
    
    try:
        user_id = parts[2]
    except:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            user_id = message.from_user.id
    
    user = await User.get(message.from_user.id)
    recipient = await User.get(user_id)
    nickname = user.nickname

    try:
        summ = parts[1]
        summ = summ.replace('к', '000').replace('м', '000000')
        summ = float(summ)
    except:
        await message.reply(_(
            'take_invalid_sum').format(nickname=nickname))
        return

    if not recipient:
        await message.answer(_(
            'take_user_not_found'))
        return

    await recipient.subtract_balance(summ)

    await message.reply(_(
        'take_success').format(
            nickname=nickname,
            recipient=recipient.nickname,
            summ=transform_int(summ)
        )
    )

    try:
        settings = await NotificationSettings.get(message.from_user.id)
        if settings.allow_transfers:
            await bot.send_message(user_id, _(
                'take_notify_message').format(
                    summ=transform_int(summ)
                )
            )
    except TelegramAPIError:
        await message.answer(_(
            'take_notify_failed'))