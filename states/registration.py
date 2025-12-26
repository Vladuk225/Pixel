from aiogram.fsm.state import State, StatesGroup


class RegistrationState(StatesGroup):
    enter_username = State()
    choose_gender = State()