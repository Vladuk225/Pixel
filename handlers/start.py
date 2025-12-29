from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.register import get_register_keyboard


router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, _):
    await message.answer_photo(
        photo='https://postimg.cc/NygRn3x5',
        caption=_("start"),
        reply_markup=await get_register_keyboard(message.from_user.id, _)
    )
    await message.answer('Бот был разработан <a href="https://t.me/ascendstudiotg">Ascend Studio</a>')