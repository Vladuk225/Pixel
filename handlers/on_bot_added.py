from aiogram import Router, F
from aiogram.types import Message
from utils.filters.is_bot import IsBot


router = Router()


@router.message(F.new_chat_members, IsBot)
async def on_new_member(message: Message, _):
    await message.answer(
        _("on_bot_added")
    )