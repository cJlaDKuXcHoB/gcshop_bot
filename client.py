from aiogram import types
from create_bot import dp, bot
import json
from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from handlers import keyboard
from aiogram.utils import executor
import os
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from handlers.states import AdminState, OrderState
from aiogram.types import ReplyKeyboardRemove
import asyncio
from aiogram.types import ParseMode
import math
from aiogram.dispatcher.filters.state import State, StatesGroup

ORDERS_FILE = 'orders.json'

USERS_FILE = 'users.json'

CATEGORY_CLOTHING_PRICE = 1000
CATEGORY_SHOES_PRICE = 1500
CATEGORY_ACCESSORIES_PRICE = 700
CATEGORY_OTHER_PRICE = 1000

CATEGORY_CLOTHING_PRICE_u = 3500
CATEGORY_SHOES_PRICE_u = 4000
CATEGORY_ACCESSORIES_PRICE_u = 2000
CATEGORY_OTHER_PRICE_u = 2000



ADMIN_ID_1 = 1814848272
ADMIN_ID_2 = 760682525
ADMIN_ID_3 = 785186521

CURRENCY_FILE = 'currency_data_d.json'

CURRENCY_FILE_2 = 'currency_data_y.json'


#основная клавиатура
keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = [
    types.KeyboardButton(text="Рассчет заказа"),
    types.KeyboardButton(text="Отследить заказ")
    ]
keyboard_markup.add(*buttons)



#start
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    user_id = message.from_user.id
    add_user_to_file(user_id)
    await message.answer("Привет! Это бот GeekCliqueShop. Я помогу тебе оформить заказ и рассчитать его стоимость. Наш канал: @geekcliqueshop", reply_markup=ReplyKeyboardRemove())
    
    await message.answer("Выберите действие:", reply_markup=keyboard_markup)


###



#обработчик ввода категории
@dp.message_handler(state=OrderState.ENTERING_QUANTITY)
async def enter_quantity(message: types.Message, state: FSMContext):
    try:
        quantity = int(message.text)
        await state.update_data(quantity=quantity)
        await message.answer("Введите стоимость вашего заказа в юанях")
        await OrderState.ENTERING_AMOUNT.set()
    except ValueError:
        await message.answer("Некорректное значение. Введите число.")

@dp.message_handler(state=OrderState.ENTERING_QUANTITY_USA_EUROPE)
async def enter_quantity_usa_europe(message: types.Message, state: FSMContext):
    try:
        quantity = int(message.text)
        await state.update_data(quantity=quantity)
        await message.answer("Введите стоимость вашего заказа в долларах")
        await OrderState.ENTERING_AMOUNT.set()
    except ValueError:
        await message.answer("Некорректное значение. Введите число.")

@dp.callback_query_handler(lambda query: query.data.startswith("category_"), state=OrderState.ENTERING_QUANTITY_USA_EUROPE)
async def handle_category_usa_europe(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    category = callback_query.data.replace("category_", "")
    await state.update_data(category=category) 
    await state.update_data(country="usa_europe")
    await bot.send_message(callback_query.from_user.id, "Введите количество позиций в выбранной категории")
    await OrderState.ENTERING_QUANTITY_USA_EUROPE.set()


@dp.callback_query_handler(lambda query: query.data.startswith("category_"), state=OrderState.ENTERING_QUANTITY)
async def handle_category_china(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    category = callback_query.data.replace("category_", "")
    await state.update_data(category=category)
    await state.update_data(country="china")
    await bot.send_message(callback_query.from_user.id, "Введите количество позиций в выбранной категории")
    await OrderState.ENTERING_QUANTITY.set()



#клавиатура категорий
categories_keyboard = InlineKeyboardMarkup(row_width=2)
categories_keyboard.add(
    InlineKeyboardButton(text="Одежда", callback_data="category_clothing"),
    InlineKeyboardButton(text="Обувь", callback_data="category_shoes"),
    InlineKeyboardButton(text="Аксессуары", callback_data="category_accessories"),
    InlineKeyboardButton(text="Прочее", callback_data="category_other")
)


@dp.callback_query_handler(lambda query: query.data == "calculate_usa_europe")
async def handle_calculate_usa_europe(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Выберите категорию товара:", reply_markup=categories_keyboard)
    await OrderState.ENTERING_QUANTITY_USA_EUROPE.set()


#CATEGORY.SET

@dp.callback_query_handler(lambda query: query.data == "category_clothing")
async def handle_category_shoes(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda query: query.data == "category_shoes")
async def handle_category_shoes(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda query: query.data == "category_accessories")
async def handle_category_accessories(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda query: query.data == "category_other")
async def handle_category_other(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

###
    


#клавиатура выбора страны

country_keyboard = InlineKeyboardMarkup(row_width=2)
button_china = InlineKeyboardButton(text="Китай", callback_data="calculate_china")
button_usa_europe = InlineKeyboardButton(text="Америка/Европа", callback_data="calculate_usa_europe")
country_keyboard.add(button_china, button_usa_europe)

@dp.message_handler(lambda message: message.text == "Рассчет заказа")
async def calculate_order(message: types.Message):
    sticker_message = await message.answer("⏳", reply_markup=types.ReplyKeyboardRemove())
    await asyncio.sleep(1)
    await bot.delete_message(chat_id=sticker_message.chat.id, message_id=sticker_message.message_id)
    await message.answer("Выберите страну, откуда хотите рассчитать заказ:", reply_markup=country_keyboard)

@dp.callback_query_handler(lambda query: query.data == "calculate_china")
async def handle_calculate_china(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Выберите категорию товара:", reply_markup=categories_keyboard)
    await OrderState.ENTERING_QUANTITY.set()


###


#CALCULATING

@dp.message_handler(state=OrderState.ENTERING_AMOUNT)
async def enter_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        data = await state.get_data()
        quantity = data.get("quantity", 1)
        category = data.get("category")
        country = data.get("country")
        category_price = get_category_price(category, country)
        currency_data = load_currency_data(country)
        if country == "china":
            yuan_rate = currency_data.get("yuan_rate")
        elif country == "usa_europe":
            dollar_rate = currency_data.get("dollar_rate")
        currency_rate = yuan_rate if country == "china" else dollar_rate

        if country == "china":
            if amount <= 100:
                coms = 300
            elif amount >100 and amount <= 300:
                coms=600
            elif amount >300 and amount <= 1000:
                coms=900
            elif amount >1000 :
                coms=1500
        elif country == "usa_europe":
            coms=1000

        if country == "china":
            cur="юанях"
        elif country == "usa_europe":
            cur="долларах"
        total_price = calculate_total_price(amount, category_price, currency_rate, coms, quantity, country)
        await message.answer(f"Стоимость вашего заказа в {cur}: {amount}\n\nОбщая стоимость с учетом доставки до Москвы: {math.ceil(total_price)}\n\nдля заказа писать @websikee\n\nОбратите внимание, что доставка из Москвы до вашего города (CDEK) оплачивается отдельно", reply_markup=keyboard_markup)
    except ValueError or amount < 0:
        await message.answer("Некорректное значение. Введите число.")
    finally:
        await state.finish()


def load_currency_data(country):
    if country == "china":
        with open(CURRENCY_FILE_2, 'r') as file:
            currency_data = json.load(file)
    elif country == "usa_europe":  
        with open(CURRENCY_FILE, 'r') as file:
            currency_data = json.load(file)
    return currency_data

def calculate_total_price(amount, category_price, currency_rate, coms, quantity, country):
    if country == "china":
        total_price = amount * currency_rate + category_price * quantity + coms
    elif country == "usa_europe":
        total_price = (amount / 0.956 + 1) * currency_rate + category_price * quantity + coms
    return total_price



def get_category_price(category, country):
    if country == "china":
        if category == "clothing":
            return CATEGORY_CLOTHING_PRICE
        elif category == "shoes":
            return CATEGORY_SHOES_PRICE
        elif category == "accessories":
            return CATEGORY_ACCESSORIES_PRICE
        elif category == "other":
            return CATEGORY_OTHER_PRICE
    elif country == "usa_europe":
        if category == "clothing":
            return CATEGORY_CLOTHING_PRICE_u
        elif category == "shoes":
            return CATEGORY_SHOES_PRICE_u
        elif category == "accessories":
            return CATEGORY_ACCESSORIES_PRICE_u
        elif category == "other":
            return CATEGORY_OTHER_PRICE_u

    return 0

###



#TRACK ORDER

@dp.message_handler(lambda message: message.text == "Отследить заказ")
async def track_order(message: types.Message):
    await message.answer("Введите номер заказа:")
    await OrderState.TRACKING_ORDER.set()


@dp.message_handler(state=OrderState.TRACKING_ORDER)
async def process_tracking_order(message: types.Message, state: FSMContext):
    order_number = message.text
    orders = load_orders()
    status = orders.get(order_number)
    if status:
        await message.answer(f"Статус вашего заказа: {status}")
    else:
        await message.answer("Заказ не найден.")
    await state.finish()

###









#ADMIN.SET.PANEL

@dp.message_handler(commands=['admin'])
async def command_admin(message: types.Message):
    if message.from_user.id in {ADMIN_ID_1, ADMIN_ID_2, ADMIN_ID_3}:
        keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [
            types.KeyboardButton(text="Изменить курс Юаня"),
            types.KeyboardButton(text="Изменить курс доллара"),
            types.KeyboardButton(text="Рассылка"),
            types.KeyboardButton(text="изменить статус"),
            types.KeyboardButton(text="создать заказ"),
            types.KeyboardButton(text="удалить заказ"),
        ]
        keyboard_markup.add(*buttons)
        await message.answer("$adm_log$", reply_markup=keyboard_markup)
    else:
        pass

###


#ADMIN.ORDER

@dp.message_handler(lambda message: message.text == "удалить заказ")
async def delete_order_command(message: types.Message):
    if message.from_user.id in {ADMIN_ID_1, ADMIN_ID_2, ADMIN_ID_3}:
        orders = load_orders()
        buttons = [InlineKeyboardButton(text=f"Удалить {num}", callback_data=f"delete_{num}") for num in orders]
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        await message.answer("Выберите заказ для удаления:", reply_markup=keyboard)
        await AdminState.DELETING_ORDER.set()
    else:
        pass


@dp.callback_query_handler(lambda c: c.data.startswith('delete_'), state=AdminState.DELETING_ORDER)
async def process_order_deletion(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    order_number = callback_query.data.replace('delete_', '')
    orders = load_orders()
    if order_number in orders:
        del orders[order_number]
        save_orders(orders)
        await bot.send_message(callback_query.from_user.id, f"Заказ {order_number} удален.")
    else:
        await bot.send_message(callback_query.from_user.id, "Заказ не найден.")
    await state.finish()


@dp.message_handler(lambda message: message.text == "создать заказ")
async def create_order_command(message: types.Message):
    if message.from_user.id in {ADMIN_ID_1, ADMIN_ID_2, ADMIN_ID_3}:
        await message.answer("Введите номер нового заказа:")
        await AdminState.CREATING_NEW_ORDER.set()
    else:
        pass

@dp.message_handler(state=AdminState.CREATING_NEW_ORDER)
async def process_new_order_number(message: types.Message, state: FSMContext):
    order_number = message.text
    await state.update_data(order_number=order_number)
    await message.answer("Введите статус нового заказа:")
    await AdminState.ENTERING_NEW_ORDER_STATUS.set()

@dp.message_handler(state=AdminState.ENTERING_NEW_ORDER_STATUS)
async def process_new_order_status(message: types.Message, state: FSMContext):
    new_status = message.text
    data = await state.get_data()
    order_number = data['order_number']
    orders = load_orders()
    orders[order_number] = new_status
    save_orders(orders)
    await message.answer("Новый заказ создан.")
    await state.finish()

@dp.message_handler(lambda message: message.text == "изменить статус")
async def change_order_status_command(message: types.Message):
    if message.from_user.id in {ADMIN_ID_1, ADMIN_ID_2, ADMIN_ID_3}:
        orders = load_orders()
        buttons = [InlineKeyboardButton(text=num, callback_data=num) for num in orders]
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await message.answer("Выберите заказ для изменения статуса:", reply_markup=keyboard)
        await AdminState.CHANGING_ORDER_STATUS.set()


@dp.callback_query_handler(state=AdminState.CHANGING_ORDER_STATUS)
async def change_order_status(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await state.update_data(order_number=callback_query.data)
    await bot.send_message(callback_query.from_user.id, "Введите новый статус заказа:")
    await AdminState.ENTERING_NEW_STATUS.set()


@dp.message_handler(state=AdminState.ENTERING_NEW_STATUS)
async def process_new_status(message: types.Message, state: FSMContext):
    new_status = message.text
    data = await state.get_data()
    order_number = data['order_number']
    orders = load_orders()
    orders[order_number] = new_status
    save_orders(orders)
    await message.answer("Статус заказа обновлен.")
    await state.finish()



def load_orders():
    try:
        with open(ORDERS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_orders(orders):
    with open(ORDERS_FILE, 'w', encoding='utf-8') as file:
        json.dump(orders, file)

###
        



#EDITING CNY RATE
@dp.message_handler(lambda message: message.text == "Изменить курс Юаня", state=None)
async def change_yuan_rate(message: types.Message):
    if message.from_user.id in {ADMIN_ID_1, ADMIN_ID_2, ADMIN_ID_3}:
    
        await AdminState.waiting_for_rate.set()
        await message.answer("Введите новый курс Юаня:")
    else:
        pass
    
@dp.message_handler(state=AdminState.waiting_for_rate, content_types=types.ContentType.TEXT)
async def process_change_yuan_rate(message: types.Message, state: FSMContext):
    try:
        new_rate = float(message.text)
        write_new_rate_to_json(new_rate)
        await bot.send_message(ADMIN_ID_1, f"Админ {message.from_user.username} изменил курс Юаня на {new_rate}")
        await bot.send_message(ADMIN_ID_2, f"Админ {message.from_user.username} изменил курс Юаня на {new_rate}")
        await bot.send_message(ADMIN_ID_3, f"Админ {message.from_user.username} изменил курс Юаня на {new_rate}")
        await message.answer(f"Курс Юаня успешно изменен: {new_rate}")
    except ValueError:
        await message.answer("Некорректное значение. Введите число.")
    finally:
        await state.finish()

def write_new_rate_to_json(new_rate: float):
    with open(CURRENCY_FILE_2, 'w') as file:
        json.dump({"yuan_rate": new_rate}, file)

###






#EDITING USD RATE

@dp.message_handler(lambda message: message.text == "Изменить курс доллара", state=None)
async def change_dollar_rate(message: types.Message):
    if message.from_user.id in {ADMIN_ID_1, ADMIN_ID_2, ADMIN_ID_3}:
        await AdminState.waiting_for_dollar_rate.set()
        await message.answer("Введите новый курс доллара:")
    else:
        pass

@dp.message_handler(state=AdminState.waiting_for_dollar_rate, content_types=types.ContentType.TEXT)
async def process_change_dollar_rate(message: types.Message, state: FSMContext):
    try:
        new_rate = float(message.text)
        write_new_dollar_rate_to_json(new_rate)
        await bot.send_message(ADMIN_ID_1, f"Админ {message.from_user.username} изменил курс доллара на {new_rate}")
        await bot.send_message(ADMIN_ID_2, f"Админ {message.from_user.username} изменил курс доллара на {new_rate}")
        await bot.send_message(ADMIN_ID_3, f"Админ {message.from_user.username} изменил курс доллара на {new_rate}")
        await message.answer(f"Курс доллара успешно изменен: {new_rate}")
    except ValueError:
        await message.answer("Некорректное значение. Введите число.")
    finally:
        await state.finish()

def write_new_dollar_rate_to_json(new_rate: float):
    with open(CURRENCY_FILE, 'w') as file:
        json.dump({"dollar_rate": new_rate}, file)

###

#SEND.MESSAGE

@dp.message_handler(lambda message: message.text == "Рассылка")
async def send_broadcast(message: types.Message, state: FSMContext):
    if message.from_user.id in {ADMIN_ID_1, ADMIN_ID_2, ADMIN_ID_3}:
        await AdminState.waiting_for_broadcast.set()
        await message.answer("введите сообщение для рассылки:")
    else:
        pass
@dp.message_handler(state=AdminState.waiting_for_broadcast)
async def process_broadcast(message: types.Message, state: FSMContext):
    try:
        broadcast_message = message.text

        users = get_users_from_file()

        for user_id in users:
            try:
                await bot.send_message(user_id, broadcast_message)
            except Exception as e:
                await bot.send_message(ADMIN_ID_1, f"ошибка: {user_id} {e}")
                await bot.send_message(ADMIN_ID_2, f"ошибка: {user_id} {e}")
                await bot.send_message(ADMIN_ID_3, f"ошибка: {user_id} {e}")

        await message.answer(f"отправлено.")
    except Exception as e:
        await bot.send_message(ADMIN_ID_1, f"ошибка: {e}")
        await bot.send_message(ADMIN_ID_2, f"ошибка: {e}")
        await bot.send_message(ADMIN_ID_3, f"ошибка: {e}")
    finally:
        await state.finish()


def get_users_from_file():
    try:
        with open(USERS_FILE, 'r') as file:
            users = json.load(file)
        return users if users else []
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []

def add_user_to_file(user_id):
    users = get_users_from_file()
    if user_id not in users:
        users.append(user_id)
        with open(USERS_FILE, 'w') as file:
            json.dump(users, file)



###