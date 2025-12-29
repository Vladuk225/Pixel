from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from utils.filters.startswith import TextStartsWith, CallbackDataStartsWith
from utils.unauthorized_messages import get_random_unauthorized_message
from middlewares.i18n import I18nMiddleware
from keyboards.shop import shop_kb, bonus_buy_kb
from database.user import User
from database.bonus import BonusDB


router = Router()
i18n_middleware = I18nMiddleware()


@router.callback_query(F.data.startswith("shop"))
async def shop_menu(call: CallbackQuery, _):
    val, user_id_str = call.data.split(":")
    if not call.from_user.id == int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    await call.message.delete()
    await call.message.answer(text=_("shop_btn_text"), reply_markup=await shop_kb(call.from_user.id, _))


@router.callback_query(F.data.startswith("bonus_info"))
async def shop_menu(call: CallbackQuery, _):
    val, user_id_str = call.data.split(":")
    if not call.from_user.id == int(user_id_str):
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)
    val, val, num = call.data.split('_')
    num = int(num.split(':')[0])
    print(num)
    bonus_amounts = {
        2: [600, 200, 400],
        3: [2500, 800, 1500]
    }
    bonus_amount = list(bonus_amounts.get(num))
    print(bonus_amount)
    await call.message.delete()
    await call.message.answer(
        text=_("shop_bonus_info_text").format(
            num=num,
            cost=bonus_amount[0],
            min_amount=bonus_amount[1],
            max_amount=bonus_amount[2]
        ),
        reply_markup=bonus_buy_kb(call.from_user.id, _, num)
    )


@router.callback_query(F.data.startswith("buy_bonus"))
async def buy_bonus(call: CallbackQuery, _):
    parts = call.data.split(":")

    user_id_str = parts[1]
    val, val, bonus_num_str = parts[0].split('_')
    user_id = int(user_id_str)
    bonus_num = int(bonus_num_str)

    if call.from_user.id != user_id:
        _caller = await i18n_middleware.get_localizer_for_user(call.from_user.id)
        msg = get_random_unauthorized_message(_caller)
        return await call.answer(msg, show_alert=True)

    user = await User.get(user_id)
    if not user:
        return await call.answer("❌ Пользователь не найден.", show_alert=True)

    balance = user.balance

    bonus_costs = {
        2: 600,
        3: 2500
    }
    cost = bonus_costs.get(bonus_num)
    if cost is None:
        return await call.answer(_("buy_bonus_invalid").format(num=bonus_num), show_alert=True)

    if balance < cost:
        return await call.answer(_("buy_bonus_not_enough").format(num=bonus_num), show_alert=True)

    await user.subtract_balance(cost)

    bonus_db = BonusDB()
    await bonus_db.set_bonus_flags(user_id, **{f"has_b{bonus_num}": True})

    await call.message.delete()
    await call.message.answer(
        text=_("buy_bonus_success").format(num=bonus_num, cost=cost)
    )