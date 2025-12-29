from aiogram import Router, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from utils.filters.text_in import TextIn
from utils.emojis import random_lose_emojis


router = Router()


@router.message(Command("id"))
@router.message(TextIn([
    'узнать ид',
    'get id'
]))
async def get_user_id(message: Message, _):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        return await message.answer(f"{_('get_id_reply')}: <code>{user.id}</code>")

    args = message.text.split()
    if len(args) >= 2:
        username = args[1]

        if username.startswith("@"):
            username = username[1:]

        try:
            user = await message.bot.get_chat(username)
            return await message.answer(f"{_('get_id_username')}: <code>{user.id}</code>")
        except TelegramBadRequest:
            return await message.answer(f"{await random_lose_emojis()} {_('get_id_not_found')}")

    return await message.answer(f"{_('get_id_your')}: <code>{message.from_user.id}</code>")