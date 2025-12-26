from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from middlewares.last_active import LastActiveMiddleware
from middlewares.ban import BanMiddleware
from middlewares.register import RegisterChatMiddleware
from database.chat import Chat
from middlewares.i18n import I18nMiddleware


bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
        link_preview_is_disabled=True
    )
)


storage = MemoryStorage()
dp = Dispatcher(storage=MemoryStorage())


# Middlewares
i18n_middleware = I18nMiddleware()
dp.message.middleware(i18n_middleware)
dp.callback_query.middleware(i18n_middleware)
dp.message.middleware(LastActiveMiddleware("database.db"))
dp.message.middleware(BanMiddleware())
dp.callback_query.middleware(LastActiveMiddleware("database.db"))
db = Chat()
dp.message.middleware(RegisterChatMiddleware(db))