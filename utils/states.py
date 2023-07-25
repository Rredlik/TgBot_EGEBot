from typing import Final
from aiogram.dispatcher.filters.state import StatesGroup, State


class RestStates(StatesGroup):
    STATE_1_NAME: Final = State()
    STATE_2_TYPE: Final = State()
    STATE_3_KITCHEN: Final = State()
    STATE_4_DESCRIPT: Final = State()
    STATE_5_CHECK: Final = State()
    STATE_6_ADDRESS: Final = State()
    STATE_7_MENU: Final = State()
    STATE_8_VIEW: Final = State()
    STATE_9_IMAGE: Final = State()


class ChooseStages(StatesGroup):
    CHOOSE_1: Final = State()
    CHOOSE_2: Final = State()
    CHOOSE_3: Final = State()


class ADPosting(StatesGroup):
    WriteText: Final = State()
    CheckPost: Final = State()
    SendPost: Final = State()
