from aiogram import types, Dispatcher
from create_bot import dp, bot


async def echo_send(message : types.Message):
	await message.reply('Я не знаю что на это ответить😢 \n \nВоспользуйтесь командой /menu')

#Регистраци хендов
def register_handlers_other(dp : Dispatcher):
	dp.register_message_handler(echo_send)
