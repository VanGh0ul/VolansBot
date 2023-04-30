from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from datetime import datetime 
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from aiogram.utils import markdown as md
from google.oauth2 import service_account
from googleapiclient.discovery import build
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
import random
import requests
import telebot
import json
import os
import pytz


class FSMUanPrice(StatesGroup):
    GlobalUan = State()


class FSMDelivery(StatesGroup):
    Sneakers                  = State()
    Electronic                = State()
    LightThings               = State()
    HeavyThings               = State()

    Price                     = State()
    Number_of_items           = State()
    Article_code              = State()
    Whats_a_button            = State()
    Order_summary             = State()
    Сharacteristic            = State()
    Buyer_FIO                 = State()

class FSMCalc(StatesGroup):
    Calculate = State()


GlobalUanPrice = 12.5


def generate_random_code():
    # генерируем 2 случайных символа
    letters = [chr(random.randint(65, 90)) for _ in range(4)]
    # генерируем 4 случайных цифры
    numbers = [str(random.randint(0, 9)) for _ in range(4)]
    # объединяем символы и цифры в формате AAAA-1234
    return ''.join(letters) + '-' + ''.join(numbers)


#Стартовое меню
async def command_start(message: types.Message):
        # добавляем инлайн кнопку
        inline_button_WhyPoison = InlineKeyboardButton("Почему Poizon 🔭", callback_data="why_poizon")
        inline_button_PoisonInstruction  = InlineKeyboardButton("Инструкция по Poizon 📋", url="https://vk.com/@volans_store-kak-naiti-tovar-i-sdelat-zakaz-v-prilozhenii-poizon")
        inline_button_deliveryInfo = InlineKeyboardButton("Доставка ✈️", callback_data="delivery_info")
        inline_button_teamInfo = InlineKeyboardButton("О нас ❗️", callback_data="team_info")
        inline_button_mainMenu = InlineKeyboardButton("Основная информация о сообществе ⤵️", callback_data="main_menu")

        inline_button_feedack= types.InlineKeyboardButton(text='Отзывы 💌', url="https://vk.com/hydrogen17?w=wall290022421_953%2Fall")
        inline_button_calculate_VK_url= types.InlineKeyboardButton(text='Группа в вк 👥', url="https://vk.com/volans_store")

        inline_keyboard_Start = InlineKeyboardMarkup().add(inline_button_WhyPoison).add(inline_button_PoisonInstruction).row(inline_button_calculate_VK_url,inline_button_feedack).row(inline_button_deliveryInfo,inline_button_teamInfo).add(inline_button_mainMenu)

        img = open('img/startimg.png', 'rb')
       
        user_username = message.from_user.username
        user_link = md.quote_html(user_username)
        print(user_link)
        await bot.send_photo(message.from_user.id, img,
                                'Приветствую, ' + user_link + "👋🏻" +
                                "\n\n" +
                                "Команда Volans Store приветствует тебя в нашем Телеграм-боте!"
                                "\n\n" +
                                "Сложная политическая и экономическая ситуация в России привела к тому, что людям стало трудно позволить себе приобретать любимые вещи по разумным ценам." +
                                "\n\n" +
                                "Мы стремимся исправить эту проблему!" + 
                                "\n" + 
                                "Мы предоставляем нашим клиентам простой и быстрый способ выкупа и доставки товаров из Китая в Россию."+
                                "\n" +
                                "Наша миссия - обеспечить удобство и доступность для наших клиентов."
                                "\n\n" +
                                "Только оригинал.\n" +
                                "Перед тем, как Ваш заказ будет доставлен, он пройдет тщательную проверку специальной инспекцией на площадке , а затем повторно нашей командой.\n"+
                                "Нам кажется, что именно благодаря этому функционалу люди со всего мира совершают миллионы покупок с данной площадки ежедневно."
                                "\n\n\n"+ 
                                "<b>Важная информация:</b>"
                                ,
                                parse_mode='HTML',
                                reply_markup=inline_keyboard_Start)


# Смена курса
async def command_GlobalUanChange(message: types.Message):
    # добавляем инлайн кнопку
    inline_button_backToStartMenu = InlineKeyboardButton("Вернуться в основное меню ⤵️", callback_data="main_menu")
    inline_keyboard_mainMenu = InlineKeyboardMarkup().add(inline_button_backToStartMenu)

    await bot.send_message(message.from_user.id, "<b>Укажи новый курс ¥:</b>", parse_mode='HTML', reply_markup=inline_keyboard_mainMenu)
    await FSMUanPrice.GlobalUan.set()

# Смена ввода
@dp.message_handler(state=FSMUanPrice.GlobalUan)
async def process_GlobalUan(message: types.Message, state: FSMContext):
    global GlobalUanPrice  # добавляем global для того, чтобы изменять глобальную переменную
    data = await state.get_data()
    UanPrice = data.get('UanPrice')

    inline_button_backToStartMenu = InlineKeyboardButton("Вернуться в основное меню ⤵️", callback_data="main_menu")

    inline_keyboard_mainMenu = InlineKeyboardMarkup().add(inline_button_backToStartMenu)

    try:
        GlobalUan = float(message.text)
        GlobalUanPrice = GlobalUan
        print(GlobalUanPrice)
        await bot.send_message(message.from_user.id, "<b>Текущий курс: </b>" + str(GlobalUanPrice) + " ₽", parse_mode='HTML', reply_markup=inline_keyboard_mainMenu)
        await state.finish()
    except ValueError:
        await message.reply('❌Данные введены некорректно!\nВведите число:')

#Стартовое меню
async def command_menu(message: types.Message):
   # добавляем инлайн кнопку
   inline_button_orderMenu = InlineKeyboardButton("Раздел для заказов 🛍", callback_data="order_menu")
   inline_button_uanPrice = InlineKeyboardButton("Курс Юаня 💹", callback_data="uan_price")
   inline_button_calculatePrice = InlineKeyboardButton("Калькулятор 📱", callback_data="calculate_price")
   inline_button_calculate_VK_url= types.InlineKeyboardButton(text='Подборка товаров с Poizon ❤️‍🔥', url="https://vk.com/volans_store")
   inline_button_question = InlineKeyboardButton("Вопросы менеджеру 👨‍💻", callback_data="to_manager")
   inline_button_backToStartMenu = InlineKeyboardButton("Вернуться к начальному меню ⤵️", callback_data="back_To_Start_Menu")

   inline_keyboard_mainMenu = InlineKeyboardMarkup().add(inline_button_orderMenu).row(inline_button_uanPrice,inline_button_calculatePrice).add(inline_button_calculate_VK_url).add(inline_button_question).add(inline_button_backToStartMenu)

   img = open('img/menuimg.png', 'rb')

   await bot.send_photo(message.from_user.id, img, "Наш "+
                                                                   "<a href='https://t.me/volans_store'>канал</a>" +
                                                                    " в Телеграм", parse_mode='HTML', reply_markup=inline_keyboard_mainMenu)

#Основное меню
@dp.callback_query_handler(lambda c: c.data == 'main_menu')
async def process_callback_main_menu(callback_query_main_menu: types.CallbackQuery, state: FSMContext):
   await bot.answer_callback_query(callback_query_main_menu.id)
   # добавляем инлайн кнопку
   inline_button_orderMenu = InlineKeyboardButton("Раздел для заказов 🛍", callback_data="order_menu")
   inline_button_uanPrice = InlineKeyboardButton("Курс Юаня 💹", callback_data="uan_price")
   inline_button_calculatePrice = InlineKeyboardButton("Калькулятор 📱", callback_data="calculate_price")
   inline_button_calculate_VK_url= types.InlineKeyboardButton(text='Подборка товаров с Poizon ❤️‍🔥', url="https://vk.com/volans_store")
   inline_button_question = InlineKeyboardButton("Вопросы менеджеру 👨‍💻", callback_data="to_manager")
   inline_button_backToStartMenu = InlineKeyboardButton("Основная информация о сообществе ⤵️", callback_data="back_To_Start_Menu")

   inline_keyboard_mainMenu = InlineKeyboardMarkup().add(inline_button_orderMenu).row(inline_button_uanPrice,inline_button_calculatePrice).add(inline_button_calculate_VK_url).add(inline_button_question).add(inline_button_backToStartMenu)

   img = open('img/menuimg.png', 'rb')

   await bot.send_photo(callback_query_main_menu.from_user.id, img, "Наш "+
                                                                   "<a href='https://t.me/volans_store'>канал</a>" +
                                                                    " в Телеграм", parse_mode='HTML', reply_markup=inline_keyboard_mainMenu)

#Меню заказов
@dp.callback_query_handler(lambda c: c.data == 'order_menu')
async def process_callback_order_menu(callback_query_order_menu: types.CallbackQuery, state: FSMContext):
   await bot.answer_callback_query(callback_query_order_menu.id)
   async with state.proxy() as data:
         await state.finish()
   # добавляем инлайн кнопку
   inline_button_sneakers43low = InlineKeyboardButton("Обувь 👟(до 43EU)", callback_data="sneakers_43low")
   inline_button_sneakers43more = InlineKeyboardButton("Обувь 👟(свыше 43EU)", callback_data="sneakers_43more")
   inline_button_lightThings = InlineKeyboardButton("Футболки, шорты, легкие вещи", callback_data="lightThings")
   inline_button_heavyThings = InlineKeyboardButton("Верхняя одежда, штаны, рюкзаки", callback_data="heavyThings")
   inline_button_wholesale_order = InlineKeyboardButton("Оптовый заказ 🚛", callback_data="wholesale_order")

   inline_button_backToStartMenu = InlineKeyboardButton("Вернуться в основное меню ⤴️", callback_data="main_menu")

   inline_keyboard_mainMenu = InlineKeyboardMarkup().row(inline_button_sneakers43low,inline_button_sneakers43more).add(inline_button_lightThings).add(inline_button_heavyThings).add(inline_button_wholesale_order).add(inline_button_backToStartMenu)

   img = open('img/orderMenuImg.png', 'rb')

   await bot.send_photo(callback_query_order_menu.from_user.id, img,"<b>Выберите категорию:</b>", parse_mode='HTML', reply_markup=inline_keyboard_mainMenu)

#Юань цена
@dp.callback_query_handler(lambda c: c.data == 'uan_price')
async def process_callback_uan_price(callback_query_uan_price: types.CallbackQuery, state: FSMContext):
   await bot.answer_callback_query(callback_query_uan_price.id)

   # добавляем инлайн кнопку

   inline_button_backToStartMenu = InlineKeyboardButton("Вернуться в основное меню ⤵️", callback_data="main_menu")

   inline_keyboard_mainMenu = InlineKeyboardMarkup().add(inline_button_backToStartMenu)

   img = open('img/uanPriceImg.png', 'rb')

   await bot.send_photo(callback_query_uan_price.from_user.id, img, "<b>Текущий курс: </b>" + str(GlobalUanPrice) + " ₽", parse_mode='HTML', reply_markup=inline_keyboard_mainMenu)

@dp.callback_query_handler(lambda c: c.data == 'why_poizon')
async def process_callback_why_poizon(callback_query_why_poizon: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_why_poizon.id)
    # добавляем инлайн кнопку
    inline_button_why_poizon = InlineKeyboardButton("Назад 🔙", callback_data="back_To_Start_Menu")

    inline_keyboard_Start = InlineKeyboardMarkup().add(inline_button_why_poizon)

    img = open('img/why_poizon.png', 'rb')
   
    await bot.send_photo(callback_query_why_poizon.from_user.id, img,
                                "Dewu, также известное как Poizon, - это приложение для онлайн покупок, запущенное Shanghai Shizhuang Information Technology Co., Ltd." +
                                "\n\n" +
                                "Основанная на традиционной модели электронной коммерции, китайская платформа предоставляет услуги по аутентификации и проверке продуктов для борьбы с подделками." +
                                "\n\n" +
                                "Уникальной особенностью продаж Dewu является процесс покупки сначала идентификация, отправка позже." +
                                "\n\n" +
                                "Категории продуктов охватывают модную обувь, моду, часы, аксессуары, игры, цифровую и бытовую технику, красоту, автомобили и многое другое."
                                ,
                                parse_mode='HTML',
                                reply_markup=inline_keyboard_Start)

#Доставка
@dp.callback_query_handler(lambda c: c.data == 'delivery_info')
async def process_callback_delivery_info(callback_query_delivery_info: types.CallbackQuery, state: FSMContext):
   await bot.answer_callback_query(callback_query_delivery_info.id)
   # добавляем инлайн кнопку
   inline_button_why_poizon = InlineKeyboardButton("Назад 🔙", callback_data="back_To_Start_Menu")

   inline_keyboard_Start = InlineKeyboardMarkup().add(inline_button_why_poizon)

   img = open('img/deliveryImg.png', 'rb')

   await bot.send_photo(callback_query_delivery_info.from_user.id, img, 
                                                                        "Время доставки до Москвы с момента отправки со склада в Китае:\n" +
                                                                        "🚚10-14 дней\n\n" +
                                                                        "Ниже представлены ориентировочные цены стандартной доставки \n" +
                                                                        "(Ускоренная авиа-доставка обсужается с менеджером) \n\n" +
                                                                        "Обувь\n" +
                                                                        "До 43EU 1.900₽\n" +
                                                                        "Свыше 43EU 2.200₽\n\n" +
                                                                        "Одежда\n" +
                                                                        "Футболки, шорты 1.300₽  \n" +
                                                                        "Верхняя одежда, штаны, рюкзаки 1.500₽\n" +
                                                                        "*за одну единицу товара❗️\n\n" +
                                                                        "Страховка заказов\n"+
                                                                        "Каждый товар полностью застрахован и надежно упакован\n"+
                                                                        "Цена страховки электроники составляет +5% к стоимости товара."
                                                                        ,
                                                                        parse_mode='HTML', reply_markup=inline_keyboard_Start)
                                                                        

#О нас
@dp.callback_query_handler(lambda c: c.data == 'team_info')
async def process_callback_team_info(callback_query_team_info: types.CallbackQuery, state: FSMContext):
   await bot.answer_callback_query(callback_query_team_info.id)
   # добавляем инлайн кнопку
   inline_button_backToStartMenu = InlineKeyboardButton("Назад 🔙", callback_data="back_To_Start_Menu")

   inline_keyboard_mainMenu = InlineKeyboardMarkup().add(inline_button_backToStartMenu)

   img = open('img/teamInfoImg.png', 'rb')

   await bot.send_photo(callback_query_team_info.from_user.id, img, 
                                                                    "Наша команда занимается данным направлением с 2018 года!\n"+
                                                                    "Администрация сообщества имеет более 500+ положительных отзывов, ознакомиться с которыми Вы можете в разделе «Обсуждения»\n\n"+
                                                                    "В нашем магазине представлен широкий ассортимент различной одежды, обуви, аксессуаров, электроники, который представлен в разделе «Товары», более того ассортимент переодически пополняется\n"+
                                                                    "(в описании товара представлена вся актуальная информация)\n\n"+
                                                                    "Если не нашли интересующий Вас товар или же размер, у нас есть опция - заказать определенную вещь по самой выгодной цене\n\n"+
                                                                    "Если Вы являетесь постоянным клиентом или хотите оформить оптовый заказ, то мы готовы предоставить Вам особые условия по стоимости доставки и курсу оплаты\n\n"
                                                                    "Все обсуждается в индивидуальном порядке в личных сообщениях\n"
                                                                    ,parse_mode='HTML', reply_markup=inline_keyboard_mainMenu)

#Менеджер
@dp.callback_query_handler(lambda c: c.data == 'to_manager')
async def process_callback_to_manager(callback_query_to_manager: types.CallbackQuery, state: FSMContext):
   await bot.answer_callback_query(callback_query_to_manager.id)
   # добавляем инлайн кнопку
   inline_button_backToStartMenu = InlineKeyboardButton("Вернуться в основное меню ⤵️", callback_data="main_menu")

   inline_keyboard_mainMenu = InlineKeyboardMarkup().add(inline_button_backToStartMenu)

   img = open('img/managerImg.png', 'rb')

   await bot.send_photo(callback_query_to_manager.from_user.id, img,
                                                                    "Вы всегда можете написать нашему "+
                                                                    "<a href='t.me/VolansManager'>Менеджеру</a>"+
                                                                    " в Телеграм\n\n"
                                                                    "Аккаунт: " + "<a href='t.me/VolansManager'>@VolansManager</a>"
                                                                    , parse_mode='HTML', reply_markup=inline_keyboard_mainMenu)

#Менеджер
@dp.callback_query_handler(lambda c: c.data == 'wholesale_order')
async def process_callback_to_manager(callback_query_to_manager: types.CallbackQuery, state: FSMContext):
   await bot.answer_callback_query(callback_query_to_manager.id)
   # добавляем инлайн кнопку
   inline_button_backToStartMenu = InlineKeyboardButton("Вернуться в основное меню ⤵️", callback_data="main_menu")

   inline_keyboard_mainMenu = InlineKeyboardMarkup().add(inline_button_backToStartMenu)

   img = open('img/managerImg.png', 'rb')

   await bot.send_photo(callback_query_to_manager.from_user.id, img,
                                                                    "Вы всегда можете написать нашему "+
                                                                    "<a href='t.me/VolansManager'>Менеджеру</a>"+
                                                                    " в Телеграм\n\n"
                                                                    "Аккаунт: " + "<a href='t.me/VolansManager'>@VolansManager</a>"
                                                                    , parse_mode='HTML', reply_markup=inline_keyboard_mainMenu) 

#Калькулятор
@dp.callback_query_handler(lambda c: c.data == 'calculate_price')
async def process_callback_calculate_price(callback_query_calculate_price: types.CallbackQuery, state: FSMContext):
   await bot.answer_callback_query(callback_query_calculate_price.id)
   # добавляем инлайн кнопку
   inline_button_backToStartMenu = InlineKeyboardButton("Назад 🔙", callback_data="cancel_calc")

   inline_keyboard_mainMenu = InlineKeyboardMarkup().add(inline_button_backToStartMenu)
   
   img = open('img/howToOrderImg.png', 'rb')

   await bot.send_message(callback_query_calculate_price.from_user.id, "<b>Укажите сумму для первода из CNY в RUB: </b>", parse_mode='HTML', reply_markup=inline_keyboard_mainMenu)
   await FSMCalc.Calculate.set()

# Получаем ответ на вопрос о подсчете
@dp.message_handler(state=FSMCalc.Calculate)
async def process_Calculate(message: types.Message, state: FSMContext):
   
    data = await state.get_data()
    calc_Sum = data.get('calc_Sum')

    inline_button_backToStartMenu = InlineKeyboardButton("Назад 🔙", callback_data="cancel_calc")

    inline_keyboard_mainMenu = InlineKeyboardMarkup().add(inline_button_backToStartMenu)

    try:
        Last_Sum = round(float(message.text) * GlobalUanPrice, 2)
        if not message.text.isdigit():
            return
        await bot.send_message(message.from_user.id, "✅<b>Итог: </b>" + str(Last_Sum) + " ₽" + 
                                                                                              "\n<i>*Сумма без учета доставки в Москву</i>"
                                                                                              ,
                                                                                              parse_mode='HTML',reply_markup=inline_keyboard_mainMenu)
    except ValueError:
        await message.reply('❌Данные введены не корректно!\nВведите число:')

# Обработчик коллбеков для кнопки "Отменить" в состоянии 
@dp.callback_query_handler(lambda c: c.data == 'cancel_calc', state=[FSMCalc.Calculate])
async def process_callback_cancel_calc(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await state.finish()
    await process_callback_main_menu(callback_query, state)


# Обработчик коллбеков для кнопки "Отменить" в состоянии 
@dp.callback_query_handler(lambda c: c.data == 'cancel_order', state=[FSMDelivery.Price, FSMDelivery.Number_of_items, FSMDelivery.Article_code, FSMDelivery.Whats_a_button, FSMDelivery.Order_summary, FSMDelivery.Сharacteristic, FSMDelivery.Buyer_FIO])
async def process_callback_cancel_order(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await state.finish()
    await process_callback_order_menu(callback_query, state)

@dp.callback_query_handler(lambda c: c.data in ['sneakers_43low','sneakers_43more', 'lightThings', 'heavyThings'], types.Message)
async def process_callback_delivery(callback_query_delivery: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query_delivery.id)
     # получаем выбранный тип доставки
    delivery_type = callback_query_delivery.data

    inline_button_closeOrder = InlineKeyboardButton("Отменить 🚫", callback_data="cancel_order")

    inline_keyboard_backToMenu = InlineKeyboardMarkup().add(inline_button_closeOrder)


    # узнаем цену доставки в зависимости от выбранного типа доставки
    delivery_price = 0
    if delivery_type == 'sneakers_43low':
        delivery_price = 1900
        await bot.send_message(callback_query_delivery.from_user.id, "<b>Укажите Фамилию и Имя:</b>", parse_mode='HTML', reply_markup=inline_keyboard_backToMenu)
        await FSMDelivery.Buyer_FIO.set()
        await state.update_data(delivery_price=delivery_price)
        await state.update_data(item_quantity= 1)

    elif delivery_type == 'sneakers_43more':
        delivery_price = 2200
        await bot.send_message(callback_query_delivery.from_user.id, "<b>Укажите Фамилию и Имя:</b>", parse_mode='HTML', reply_markup=inline_keyboard_backToMenu)
        await FSMDelivery.Buyer_FIO.set()
        await state.update_data(delivery_price=delivery_price)
        await state.update_data(item_quantity= 1)

    elif delivery_type == 'lightThings':
        delivery_price = 1250
        await bot.send_message(callback_query_delivery.from_user.id, "<b>Укажите Фамилию и Имя:</b>", parse_mode='HTML', reply_markup=inline_keyboard_backToMenu)
        await FSMDelivery.Buyer_FIO.set()
        await state.update_data(delivery_price=delivery_price)
        await state.update_data(item_quantity= 1)

    elif delivery_type == 'heavyThings':
        delivery_price = 1500
        await bot.send_message(callback_query_delivery.from_user.id, "<b>Укажите Фамилию и Имя:</b>", parse_mode='HTML', reply_markup=inline_keyboard_backToMenu)
        await FSMDelivery.Buyer_FIO.set()
        await state.update_data(delivery_price=delivery_price)
        await state.update_data(item_quantity= 1)



# Получаем ответ на вопрос о количестве
@dp.message_handler(state=FSMDelivery.Number_of_items)
async def process_Number_of_items(message: types.Message, state: FSMContext):
    data = await state.get_data()
    delivery_item_quantity = data.get('delivery_item_quantity')

    inline_button_closeOrder = InlineKeyboardButton("Отменить 🚫", callback_data="cancel_order")
    inline_keyboard_backToMenu = InlineKeyboardMarkup().add(inline_button_closeOrder)

    try:
        item_quantity = int(message.text)
        if not message.text.isdigit():
            return
        await state.update_data(item_quantity=item_quantity)
        await FSMDelivery.Buyer_FIO.set()
        await bot.send_message(message.from_user.id, "<b>Укажите Фамилию и Имя:</b>", parse_mode='HTML', reply_markup=inline_keyboard_backToMenu)

    except ValueError:
        await message.reply('❌Данные введены не корректно!\nВведите целое число:')

# Получаем ответ на вопрос о фио
@dp.message_handler(state=FSMDelivery.Buyer_FIO)
async def process_buyer_FIO(message: types.Message, state: FSMContext):
    data = await state.get_data()
    delivery_buyer_FIO = data.get('delivery_buyer_FIO')

    inline_button_closeOrder = InlineKeyboardButton("Отменить 🚫", callback_data="cancel_order")
    inline_keyboard_backToMenu = InlineKeyboardMarkup().add(inline_button_closeOrder)

    try:
        buyer_FIO = str(message.text)
        await state.update_data(buyer_FIO=buyer_FIO)
        await FSMDelivery.Сharacteristic.set()
        await bot.send_message(message.from_user.id, "<b>Укажите характеристику товара(например размер):</b>\n<i>*если характеристика отсутствует, так и напишите</i>", parse_mode='HTML', reply_markup=inline_keyboard_backToMenu)
    except ValueError:
        await message.reply('❌Данные введены не корректно!')

# Получаем ответ на вопрос о характеристике
@dp.message_handler(state=FSMDelivery.Сharacteristic)
async def process_Сharacteristic(message: types.Message, state: FSMContext):
    data = await state.get_data()
    delivery_item_characteristic = data.get('delivery_characteristic')

    inline_button_closeOrder = InlineKeyboardButton("Отменить 🚫", callback_data="cancel_order")
    inline_keyboard_backToMenu = InlineKeyboardMarkup().add(inline_button_closeOrder)

    try:
        Сharacteristic = str(message.text)
        await state.update_data(Сharacteristic=Сharacteristic)
        await FSMDelivery.Price.set()
        await bot.send_message(message.from_user.id, "<b>Укажите цену в ¥ за 1 единицу:</b>", parse_mode='HTML', reply_markup=inline_keyboard_backToMenu)
    except ValueError:
        await message.reply('❌Данные введены не корректно!\nВведите число:')

# Получаем ответ на вопрос о цене
@dp.message_handler(state=FSMDelivery.Price)
async def process_wholesale_Price(message: types.Message, state: FSMContext):

    try:
        data = await state.get_data()
        delivery_item_price = data.get('delivery_item_price')

        inline_button_closeOrder = InlineKeyboardButton("Отменить 🚫", callback_data="cancel_order")
        inline_keyboard_backToMenu = InlineKeyboardMarkup().add(inline_button_closeOrder)

        try:
            item_price = float(message.text)
            if not message.text.isdigit():
                return
            await state.update_data(item_price=item_price)

            await FSMDelivery.Article_code.set()
            await bot.send_message(message.from_user.id, "<b>Укажите артикул товара</b>", parse_mode='HTML', reply_markup=inline_keyboard_backToMenu)

        except ValueError:
            await message.reply('❌Данные введены не корректно!\nВведите число:')

    except ValueError:
            await message.reply('❌Данные введены не корректно!\nВведите число:')

# Получаем ответ на вопрос об артикле
@dp.message_handler(state=FSMDelivery.Article_code)
async def process_Article_code(message: types.Message, state: FSMContext):

    data = await state.get_data()
    delivery_article_code = data.get('delivery_article_code')

    try:
        item_article_code = str(message.text)
        await state.update_data(item_article_code=item_article_code)
        
    except ValueError:
        await message.reply('❌Данные введены не корректно!\nВведите число:')

    inline_button_closeOrder = InlineKeyboardButton("Отменить 🚫", callback_data="cancel_order")

    inline_button_emeraldButton = InlineKeyboardButton("Изумрудная кнопка 🟢", callback_data="emerald_button")
    inline_button_blackButton = InlineKeyboardButton("Черная кнопка ⚫", callback_data="black_button")

    inline_keyboard_backToMenu = InlineKeyboardMarkup().row(inline_button_emeraldButton,inline_button_blackButton).add(inline_button_closeOrder)

    await bot.send_message(message.from_user.id, "✅Выберите кнопку:", reply_markup = inline_keyboard_backToMenu)   


@dp.callback_query_handler(lambda c: c.data in ['emerald_button', 'black_button'], state=FSMDelivery.Article_code)
async def process_callback_buttonColorSelect(callback_query_buttonColorSelect: types.CallbackQuery, state: FSMContext):

    await bot.answer_callback_query(callback_query_buttonColorSelect.id)

    # Получаем выбранный цвет кнопки
    buttonColorSelect = callback_query_buttonColorSelect.data

    # Создаем inline-кнопку для отмены заказа и клавиатуру для возврата к меню
    inline_button_closeOrder = InlineKeyboardButton("Отменить 🚫", callback_data="cancel_order")
    inline_keyboard_backToMenu = InlineKeyboardMarkup().add(inline_button_closeOrder)

    if buttonColorSelect == 'emerald_button':
        button_сolor = "Изумрудная 🟢"
    elif buttonColorSelect == 'black_button':
        button_сolor = "Черная ⚫"

    # Сохраняем выбранный цвет кнопки в контексте FSM и переходим к следующему состоянию
    await state.update_data(button_сolor=button_сolor)

    data = await state.get_data()
    buyer_FIO              = data.get('buyer_FIO')
    delivery_item_quantity = data.get('item_quantity')
    Сharacteristic         = data.get('Сharacteristic')
    delivery_item_price    = data.get('item_price')
    delivery_price         = data.get('delivery_price')
    delivery_article_code  = data.get('item_article_code')
    button_сolor           = data.get('button_сolor')

    print(buyer_FIO)               # АНдрэ
    print(delivery_item_quantity)  # 1
    print(Сharacteristic)          # 42.5
    print(delivery_item_price)     # 999
    print(delivery_price)          # None
    print(delivery_article_code)   # GP-123
    print(button_сolor)            # Изумрудная 🟢

    uanAllPrice = float(delivery_item_quantity * delivery_item_price)

    rubAllPrice = float(uanAllPrice * GlobalUanPrice) + float(delivery_item_quantity * delivery_price)

    code = generate_random_code()

    user_username = callback_query_buttonColorSelect.from_user.username
    user_link = md.quote_html(user_username)

        # Установка временной зоны Москвы
    timezone = pytz.timezone('Europe/Moscow')

    # Получение текущей даты и времени в Москве
    now = datetime.now(timezone)

    # Преобразование даты в строку для вывода
    date_str = now.strftime("%d-%m-%Y %H:%M:%S")

    # Путь до файла с ключами API (замените на свой путь)
    KEY_FILE_LOCATION = 'sheets/volansstore-76f523e1755a.json'

    # ID вашей таблицы Google Sheets
    SPREADSHEET_ID = '1PGdsdkzWsjhC6UTlPjdPAaTi9XJxu5HNN1tylesAmSc'

    # Авторизация с помощью ключей API
    creds = service_account.Credentials.from_service_account_file(KEY_FILE_LOCATION, scopes=['https://www.googleapis.com/auth/spreadsheets'])

    # Подключение к Google Sheets API
    service = build('sheets', 'v4', credentials=creds)

    # Передача данных в таблицу
    values = [[date_str ,buyer_FIO, code ,delivery_item_quantity, Сharacteristic, delivery_item_price, delivery_price, delivery_article_code, button_сolor, user_link, rubAllPrice, "Не оплачено 🔴"]]
    sheet_name = 'l1'  # Название листа в таблице
    range_name = sheet_name + '!A1'  # Диапазон ячеек для записи данных
    request_body = {
        'values': values
    }
    response = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body=request_body
    ).execute()

    # Вывод сообщения об успешной записи в таблицу
    print(f'Данные успешно записаны в таблицу: {response["updates"]["updatedRange"]}')
    
    inline_button_closeOrder = InlineKeyboardButton("В меню заказов 🔙", callback_data="order_menu")

    inline_keyboard_backToMenu = InlineKeyboardMarkup().add(inline_button_closeOrder)

    img = open('img/orderInfoImg.png', 'rb')

        # Отправляем сообщение с результатом

    await bot.send_photo(callback_query_buttonColorSelect.from_user.id, img,
                                                                          f"📦 Ваш заказ: " + str(code) + "\n" + "Текущий курс " + str(GlobalUanPrice) + " 💹" + "\n\n" + 
                                                                          f"Инициалы: {buyer_FIO}\n"+
                                                                          f"Количество: {delivery_item_quantity}\n"+
                                                                          f"Характеристика: {Сharacteristic}\n"+
                                                                          f"Стоимость за единицу: {delivery_item_price} ¥\n"+
                                                                          f"Артикул: {delivery_article_code}\n"+
                                                                          f"Цвет кнопки: {button_сolor}\n\n"+
                                                                          f"Тинькофф Банк\n"+
                                                                          f"<span class='tg-spoiler'>5536913971663907</span>"+ "\n"
                                                                          f"<i>Андрей Ч.</i>\n\n" +
                                                                          f"💳Сумма к оплате: {rubAllPrice:.2f} ₽\n\n" +
                                                                          f"<b>⚠️ Не забудьте отправить нам скриншот перевода и данной карточки менеджеру: </b>" + "<a href='t.me/VolansManager'>@VolansManager</a>",
                                                                          parse_mode='HTML',reply_markup=inline_keyboard_backToMenu)

    # Очищаем данные
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'back_To_Start_Menu')
async def process_callback_back_To_Start_Menu(callback_query_back_To_Start_Menu: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_back_To_Start_Menu.id)

    # добавляем инлайн кнопку
    inline_button_WhyPoison = InlineKeyboardButton("Почему Poizon 🔭", callback_data="why_poizon")
    inline_button_PoisonInstruction  = InlineKeyboardButton("Инструкция по Poizon 📋", url="https://vk.com/@volans_store-kak-naiti-tovar-i-sdelat-zakaz-v-prilozhenii-poizon")
    inline_button_deliveryInfo = InlineKeyboardButton("Доставка ✈️", callback_data="delivery_info")
    inline_button_teamInfo = InlineKeyboardButton("О нас ❗️", callback_data="team_info")
    inline_button_mainMenu = InlineKeyboardButton("В основное меню ⤴️", callback_data="main_menu")

    inline_button_feedack= types.InlineKeyboardButton(text='Отзывы 💌', url="https://vk.com/hydrogen17?w=wall290022421_953%2Fall")
    inline_button_calculate_VK_url= types.InlineKeyboardButton(text='Группа в вк 👥', url="https://vk.com/volans_store")

    inline_keyboard_Start = InlineKeyboardMarkup().add(inline_button_WhyPoison).add(inline_button_PoisonInstruction).row(inline_button_calculate_VK_url,inline_button_feedack).row(inline_button_deliveryInfo,inline_button_teamInfo).add(inline_button_mainMenu)

    img = open('img/startimg.png', 'rb')
    user_username = callback_query_back_To_Start_Menu.from_user.username
    user_link = md.quote_html(user_username)
    print(user_link)
    await bot.send_photo(callback_query_back_To_Start_Menu.from_user.id, img,
                                                                            'Приветствую, ' + user_link + "👋🏻" +
                                                                            "\n\n" +
                                                                            "Команда Volans Store приветствует тебя в нашем Телеграм-боте!"
                                                                            "\n\n" +
                                                                            "Сложная политическая и экономическая ситуация в России привела к тому, что людям стало труднее позволить себе носить дорогие бренды одежды и приобретать товары по разумным ценам." +
                                                                            "\n\n" +
                                                                            "Мы стремимся исправить эту проблему!" + 
                                                                            "\n" + 
                                                                            "Наша компания представляет собой сервис по доставке заказов с таких площадок как 1688.com, Taobao.com, Alibaba.com, Poizon и другие известные площадки."+
                                                                            "\n" +
                                                                            "Мы предоставляем нашим клиентам простой и быстрый способ подобрать вещи и сделать заказы."+
                                                                            "\n"+"Наша миссия - обеспечить удобство и доступность для наших клиентов."
                                                                            "\n\n" +
                                                                            "Только оригинал.\n" +
                                                                            "Перед тем, как ваш заказ будет доставлен к вам, он пройдет тщательную проверку специальной инспекцией на складе, а затем будет еще раз проверен нашей командой."+
                                                                            "\n\n\n"+ 
                                                                            "<b>Важная информация:</b>"
                                                                            ,
                                                                            parse_mode='HTML',
                                                                            reply_markup=inline_keyboard_Start)


# Регистрация обработчиков
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_menu, commands=['start','help'])
    dp.register_message_handler(command_start, commands=['menu'])
    dp.register_message_handler(command_GlobalUanChange, commands=['cup'])