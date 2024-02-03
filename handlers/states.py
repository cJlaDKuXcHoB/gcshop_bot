from aiogram.dispatcher.filters.state import State, StatesGroup

class AdminState(StatesGroup):
    waiting_for_rate = State()
    waiting_for_dollar_rate = State()
    waiting_for_broadcast = State()
    CHANGING_ORDER_STATUS = State()
    ENTERING_NEW_STATUS = State()
    ENTERING_NEW_ORDER_STATUS = State()
    CREATING_NEW_ORDER = State()
    DELETING_ORDER = State()


class OrderState(StatesGroup):
    CHOOSING_CATEGORY = State()
    ENTERING_AMOUNT = State()
    ENTERING_QUANTITY = State()
    ENTERING_QUANTITY_USA_EUROPE = State()
    TRACKING_ORDER = State()
    