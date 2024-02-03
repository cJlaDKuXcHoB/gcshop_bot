# admin_handler.py

from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from create_bot import dp, bot

# main.py

ADMIN_COMMAND = 'admin'
ADMIN_USER_ID = 1814848272

# ...

@dp.message_handler(commands=[ADMIN_COMMAND])
async def admin_command(message: types.Message):
    if message.from_user.id == ADMIN_USER_ID:
        keyboard_markup = InlineKeyboardMarkup(row_width=2)
        button_send_message = InlineKeyboardButton(text='Рассылка', callback_data='admin_send_message')
        button_change_rate = InlineKeyboardButton(text='Изменить курс', callback_data='admin_change_rate')
        keyboard_markup.add(button_send_message, button_change_rate)

        await bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=keyboard_markup)
    else:
        await bot.send_message(message.from_user.id, 'Вы не являетесь администратором.')
