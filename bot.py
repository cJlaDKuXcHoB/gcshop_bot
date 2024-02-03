from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram import executor

from create_bot import dp, bot
from handlers import client


executor.start_polling(dp, skip_updates=True)