from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

TOKEN = '6041086870:AAG0yEHpybM6bPwEBg34DwDs9aKIM5QezKM'
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot,storage=storage)
















