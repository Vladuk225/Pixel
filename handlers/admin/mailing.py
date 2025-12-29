import asyncio
import numpy as np
from datetime import datetime

from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.user import Stats
from utils.filters.text_in import TextIn
from states.mailing import Rass

from keyboards.mailing import get_target_select_kb

from utils.unauthorized_messages import get_random_unauthorized_message
from decorators.admin_only import admin_only


router = Router()


@router.message(TextIn([
    'рассылка',
    'mailing'
]))
@admin_only
async def rass_menu_handler(message: Message, state: FSMContext):
    await state.set_state(Rass.post)
    await message.answer("📃 Пришлите мне сообщение для рассылки:")


@router.message(Rass.post)
async def rass_step2_handler(message: Message, state: FSMContext):
    print('попал')
    await state.set_state(Rass.kb)
    await state.update_data(msg=message)
    await message.answer("🎙️ Клавиатура (name|btn, name|btn\\n) или '-' чтобы пропустить")


@router.message(Rass.kb)
async def rass_step3_handler(message: Message, state: FSMContext, _):
    if message.text != '-':
        try:
            rows = message.text.split('\n')
            builder = InlineKeyboardBuilder()

            for row in rows:
                buttons = []
                for button in row.split(','):
                    name, url = button.strip().split('|')
                    buttons.append(
                        InlineKeyboardButton(
                            text=name.strip(),
                            url=url.strip()
                        )
                    )
                builder.row(*buttons)

            kb = builder.as_markup()
        except Exception:
            await message.answer(
                "⚠️ Неверный формат клавиатуры. Пример:\n"
                "Купить|https://url\n"
                "Поддержка|https://url"
            )
            return

        await state.update_data(kb=kb)
    else:
        await state.update_data(kb=None)

    await state.set_state(Rass.select_target)
    await state.update_data(targets=set())
    await message.answer(
        "Выберите, кому отправлять рассылку:",
        reply_markup=get_target_select_kb(set(), message.from_user.id, _)
    )


@router.callback_query(Rass.select_target)
async def handle_target_selection(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    targets = data.get("targets", set())

    if call.data == "target_users":
        targets.add("users")
    elif call.data == "target_chats":
        targets.add("chats")
    elif call.data == "target_done":
        if not targets:
            await call.answer("⚠️ Выберите хотя бы одну категорию", show_alert=True)
            return
        await state.update_data(action=targets)
        await state.set_state(Rass.time)
        await call.message.edit_text(
            "📅 Пришлите дату в формате (d.m.Y h:m) или '-' чтобы отправить сейчас."
        )
        return

    await state.update_data(targets=targets)


@router.message(Rass.time)
async def rass_finish_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    user_time = message.text
    if user_time == "-":
        scheduled_time = "сейчас"
        delay = 0
    else:
        now = datetime.now()
        if '.' not in user_time:
            user_time = f'{now.day}.{now.month}.{now.year} {user_time}'
        scheduled_time = datetime.strptime(user_time, "%d.%m.%Y %H:%M")
        delay = (scheduled_time - now).total_seconds()
        if delay < 0:
            await message.answer(
                "❗ Вы указали время в прошлом, отправка будет произведена сейчас."
            )
            delay = 0

    await message.answer(f"❤️ Рассылка была запланирована на {scheduled_time}")
    await asyncio.sleep(delay)

    targets = data.get('action', set())
    users_or_chats = set()

    if 'users' in targets:
        users_or_chats.update(await Stats.get_all_users())
    if 'chats' in targets:
        users_or_chats.update(await Stats.get_all_chats())

    users_or_chats = list(users_or_chats)
    parts = np.array_split(users_or_chats, 3)

    progress_msg = await message.answer(
        "Отправлено: 0\nУспешно: 0\nНеуспешно: 0"
    )

    index = 0
    allow = 0
    decline = 0
    msg = data.get("msg")
    kb = data.get("kb")

    for part in parts:
        for user_id in part:
            index += 1
            try:
                await msg.send_copy(chat_id=user_id, reply_markup=kb)
                allow += 1
            except Exception:
                decline += 1

        await progress_msg.edit_text(
            f"Отправлено: {index}\n"
            f"Успешно: {allow}\n"
            f"Неуспешно: {decline}"
        )

    await progress_msg.edit_text(
        f"Отправлено: {index}\n"
        f"Успешно: {allow}\n"
        f"Неуспешно: {decline}\n\n"
        f"Завершено!"
    )