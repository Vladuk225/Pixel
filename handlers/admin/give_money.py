from aiogram import Router, F
from aiogram.types import Message
from database.user import User
from utils.transform import transform_int
from aiogram.exceptions import TelegramAPIError
from bot import bot
from database.user import NotificationSettings
from utils.filters.text_in import TextIn


router = Router()


@router.message(TextIn([
    'выдать', 
    'provide'
]))
async def give_money(message: Message, _):
    print('попал')
    parts = message.text.split()
    
    try:
        user_id = parts[2]
    except IndexError:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            user_id = message.from_user.id

    user = await User.get(message.from_user.id)
    recipient = await User.get(user_id)
    nickname = user.nickname

    try:
        summ = parts[1]
        summ = summ.replace('к', '000').replace('м', '000000').replace('k', '000').replace('m', '000000')
        summ = float(summ)
    except Exception:
        await message.reply(f'''
🚫 {nickname}, {_('give_money_incorrect_amount')}

💡 {_('give_money_amount_example')}
        ''')
        return

    if not recipient:
        await message.answer(f'''
❌ {_('give_money_user_not_found')}

💡 {_('give_money_check_id')}
        ''')
        return

    await recipient.add_balance(summ)

    await message.reply(f'''
🎉 <b>{_('give_money_done')}</b>

👤 {_('give_money_from')}: <b>{nickname}</b>  
👥 {_('give_money_to')}: <b>{recipient.nickname}</b>  
💸 {_('give_money_amount')}: <b>{transform_int(summ)}ℙ</b>

✅ {_('give_money_success')}
    ''')

    try:
        settings = await NotificationSettings.get(message.from_user.id)
        if settings.allow_transfers:
            await bot.send_message(user_id, f'''
📬 {_('give_money_notify_title')}

👤 <b>{_('give_money_admin')}</b> {_('give_money_notify_text')} <b>{transform_int(summ)}ℙ</b>!

💰 {_('give_money_notify_check')}
            ''')
    except TelegramAPIError:
        await message.answer(f'''
⚠️ <b>{_('give_money_notify_failed')}</b>
{_('give_money_notify_failed_desc')}
        ''')