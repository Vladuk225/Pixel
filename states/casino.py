from aiogram.fsm.state import State, StatesGroup


class CoinGame(StatesGroup):
    waiting_for_bet = State()
    waiting_for_play = State()
    waiting_for_choice = State()

    waiting_for_opponent = State()             
    waiting_for_pvp_bet = State()              
    waiting_for_opponent_response = State()    
    waiting_for_pvp_choice = State()          
    waiting_for_pvp_flip = State()  


class SlotsGame(StatesGroup):
    waiting_for_bet = State()
    waiting_for_play = State()


class SpinGame(StatesGroup):
    waiting_for_bet = State()
    waiting_for_play = State()