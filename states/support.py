from aiogram.fsm.state import State, StatesGroup


class SupportState(StatesGroup):
    collecting_messages = State()