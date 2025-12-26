from aiogram import Router
from database.links import LinksDB
from aiogram.types import Message
from utils.filters.text_in import TextIn
from decorators.admin_only import admin_only
from utils.emojis import random_lose_emojis, random_win_emojis


router = Router()
links_db = LinksDB()  


@router.message(TextIn([
    'ссылки изменить', 
    'links update'
]))
@admin_only
async def set_link(message: Message, _):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer(f"{await random_lose_emojis()} {_('links_update_no_text')}")
        return
    link_text = parts[2]
    await links_db.set_link(link_text)
    await message.answer(f"{await random_win_emojis()} {_('links_update_saved')}")


@router.message(TextIn([
    'ссылки очистить', 
    'links clear'
]))
@admin_only
async def delete_link(message: Message, _):
    await links_db.delete_link()
    await message.answer(f"🗑 {_('links_delete_done')}")