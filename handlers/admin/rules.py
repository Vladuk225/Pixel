from aiogram import Router
from database.rules import RulesDB
from aiogram.types import Message
from utils.filters.startswith import TextStartsWith
from decorators.admin_only import admin_only
from utils.emojis import random_lose_emojis, random_win_emojis
from utils.filters.text_in import TextIn


router = Router()
rules = RulesDB()


@router.message(TextIn([
    'правила изменить', 
    'rules update'
]))
async def set_rules(message: Message, _):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer(f"{await random_lose_emojis()} {_('rules_update_no_text')}")
        return
    rule_text = parts[2]
    await rules.set_rule(rule_text)
    await message.answer(f"{await random_win_emojis()} {_('rules_update_success')}")


@router.message(TextIn([
    'правила очистить', 
    'rules clear'
]))
@admin_only
async def clear_rules(message: Message, _):
    await rules.delete_rule()
    await message.answer(f"🗑 {_('rules_delete_success')}")