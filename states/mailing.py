from aiogram.fsm.state import State, StatesGroup


class Rass(StatesGroup):
    post = State()
    kb = State()
    select_target = State()
    time = State()