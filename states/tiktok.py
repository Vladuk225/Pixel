from aiogram.fsm.state import State, StatesGroup


class TikTokState(StatesGroup):
    nickname = State()


class TikTokOptionsState(StatesGroup): 
    set_channel_name = State()
    delete_channel = State()