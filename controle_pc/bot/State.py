from aiogram.fsm.state import State, StatesGroup
class BotState(StatesGroup):
    neutral = State()
    confirmation_of_fsm_stop = State()
    waiting_for_asking_for_change_volume = State()
    processed_for_change_volume = State()
    processed_turn_on_the_sound = State()
    processed_turn_off_the_sound = State()