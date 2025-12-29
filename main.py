import asyncio
from handlers import start, on_bot_added, add_to_group, register
from handlers.admin import give_money, take_money, ban, id, rules, links, mailing
from handlers.users.basic.jobs import main as main_jobs
from handlers.users.basic.jobs import tiktok
from handlers.users.basic import faq, info, notifications, lang, transfer, shop, bonus
from handlers.users.basic.top import main, visibility
from handlers.users.games import main as game_main, flip_coin, slots, spin
from bot import bot, dp


dp.include_routers(
    start.router,
    give_money.router,
    take_money.router,
    mailing.router,
    ban.router, 
    id.router,
    add_to_group.router,
    on_bot_added.router,
    main_jobs.router,
    tiktok.router,
    register.router,
    shop.router,
    bonus.router,
    info.router,
    rules.router,
    transfer.router,
    links.router,
    notifications.router,
    visibility.router,
    main.router,
    faq.router,
    lang.router,
    game_main.router,
    flip_coin.router,
    slots.router,
    spin.router,
)


async def start_bot():
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("🛑 Бот остановлен")


if __name__ == "__main__":
    try:
#         cmd = input('>>> ')
#         if cmd.lower() in [
#  "exit", "выход",
#  "uitgang", "firi", "dalje", "መውጣት", "مخرج", "ելք", "çıxış", "ka bɔ",
#  "irten", "Izlaz", "изход", "sortida", "paggawas", "Potulukira", "出口",
#  "出口", "esce", "Izlaz", "výstup", "Afslut", "Uitgang", "eliro",
#  "väljuda", "do", "labasan", "poistu", "sortie", "útgong", "saír",
#  "გასასვლელი", "Ausfahrt", "έξοδος", "બહાર નીકળો", "sòti", "fita",
#  "puka", "יְצִיאָה", "बाहर निकलना", "tawm", "kijárat", "hætta",
#  "Ụzọ ọpụpụ", "rumuar", "KELUAR", "an slí amach", "uscita", "出口",
#  "metu", "ನಿರ್ಗಮಿಸಿ", "Шығу", "ចេញ", "gusohoka", "출구", "kɔmɔt",
#  "derî", "دەرچوون", "чыгуу", "ອອກໄປ", "exitus", "Izeja",
#  "kobima", "išeiti", "Sortie", "излез", "बाहर जानाइ", "Fivoahana",
#  "keluar", "പുറത്ത്", "ħruġ", "putanga", "बाहेर पडा", "chhuak",
#  "гарах", "ထွက်ပေါက်", "बाहिर निस्कनुहोस्", "exit", "ପ୍ରସ୍ଥାନ",
#  "ba'uu", "وتون", "خروج", "Wyjście", "saída", "ਨਿਕਾਸ",
#  "lluqsina", "Ieșire", "Выход", "ulufafo", "निर्गम", "mach",
#  "излаз", "Etsoa", "kubuda", "نڪرڻ", "පිටවීම", "VÝCHOD",
#  "izhod", "bixid", "salida", "Kaluar", "Utgång", "خرج", "veḷiyēṟu",
#  "Чыгу", "బయటకి దారి", "ทางออก", "чыгуу", "چاقىش", "Chiqish",
#  "lối ra", "allanfa", "Phuma", "אַרויסגאַנג", "Jade", "Phuma"
# ]: # пиздец)
#             raise KeyboardInterrupt
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print("🛑 Бот остановлен")
