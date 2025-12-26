from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.add_to_group import add_to_group_keyboard
from utils.filters.is_registered import IsRegisteredFilter
from utils.filters.text_in import TextIn


router = Router()


@router.message(Command("add"))
@router.message(TextIn([
    'добавить',
    'add'
]))
async def add_to_group_handler(message: Message, _):
    if not IsRegisteredFilter():
        await message.answer(
            _("not_register_filter")
        )
        return
    await message.answer(
        _("add_to_group"),
        reply_markup=add_to_group_keyboard(_)
    )