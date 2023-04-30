from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram import types
from aiogram import types,Dispatcher
from create_bot import dp, bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove	
import requests
import telebot
import json
import os

class FSMYenPrice(StatesGroup):
    Yena = State()

#Начало диалога


async def cm_start(message : types.Message):
	await FSMYenPrice.Yena.set()
	await message.reply('Введите цель поиска сотрудника:',reply_markup=types.ReplyKeyboardRemove())

#Команда старт
async def command_start(message: types.Message):
    try:
        keyboardStart = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttonbPriceCheck = ["Расчитать стоимость"]
        keyboardStart.add(*buttonbPriceCheck)

        inline_button_test = InlineKeyboardButton("Расчитать стоимость", callback_data="Расчитать стоимость")
        inline_keyboard = InlineKeyboardMarkup().add(inline_button_test)

        img = open('img/menuimg.png', 'rb')
        await bot.send_photo(message.from_user.id, img, 'Нажми кнопку для выполнения команды test',reply_markup=inline_keyboard, disable_notification=True)
        await bot.send_message(message.from_user.id, "123",reply_markup=keyboardStart)
    except:
        await bot.send_message(message.from_user.id, "Ошибка")



#Состояние 1
#Ответ от пользователя
#@dp.message_handler(state=FSMAdmin.name)

async def select_price(message : types.Message, state: FSMContext):
	async with state.proxy() as data:
		
		keyboardBack = types.ReplyKeyboardMarkup(resize_keyboard=True)
		buttonsFind = ["Найти сотрудника"]
		buttonsBack = ["Меню"]
		keyboardBack.row(*buttonsFind).add(*buttonsBack)

		data['name'] = message.text
		if message.text.isdigit():
			await message.reply('❌Данные введены не корректно!', reply_markup=keyboardBack)
			await state.finish()
			return
		await FSMYenPrice.next()
		await message.reply('Введите Фамилию сотрудника для поиска:')
	#Закончить машину состояний
		await state.finish()




def register_handlers_priceInfo(dp : Dispatcher):
	dp.register_message_handler(cm_start, lambda message: message.text == "Расчитать стоимость")
	dp.register_message_handler(command_start, lambda message: message.text == "Меню")

	dp.register_message_handler(select_price, state=FSMYenPrice.Yena)
	# dp.register_message_handler(select_agentNum, state=FSMAdmin.num)