from helpers import *

import telebot
from telebot import types
from telebot import apihelper

# 1. Инициализация бота
# apihelper.proxy = {'https': proxy}
bot = telebot.TeleBot(token)

# 2. Константы
# 2.1. Кнопки
smileSmoke = '💨 Меню кальянов'
smileDrinks = '☕️ Меню напитков'

smileCalendar = '📆 Забронировать стол'
smileBook = '📕 Меню'
smileMoney = '💸 Акции и скидки'
smileSocial = '👥 Социальные сети'
smilePhone = '📱 Контакты'
smileMap = '🚖 Как добраться'
smileEdit = '📝 Редактировать анкету'
goBack = '↩️ Вернуться назад'

# 3. Интерфейс
# 3.1. Визуальные клавиатуры
hide = types.ReplyKeyboardRemove()
hide_inline = types.InlineKeyboardMarkup()

goBackMarkup = types.ReplyKeyboardMarkup()
back = types.KeyboardButton(goBack)
goBackMarkup.row(back)

# 3.1.1. Юзерский интерфейс
userMarkup = types.ReplyKeyboardMarkup()
menuMarkup = types.ReplyKeyboardMarkup()
reviewMarkup = types.ReplyKeyboardMarkup()

# 3.1.1.1. Основной функционал
'''
Структура главного меню юзера:
        Бронь
        Меню - Акции
        Соцсети - Контакты
        Как добраться
'''
userMarkup.row(types.KeyboardButton(smileCalendar))
userMarkup.row(types.KeyboardButton(smileBook), types.KeyboardButton(smileMoney))
userMarkup.row(types.KeyboardButton(smileSocial), types.KeyboardButton(smilePhone))
userMarkup.row(types.KeyboardButton(smileMap))

# 3.1.1.2. Выбор меню
'''
Структура:
        Меню кальянов
        Меню бара
        назад
'''
menuMarkup.row(types.KeyboardButton(smileSmoke))
menuMarkup.row(types.KeyboardButton(smileDrinks))
menuMarkup.row(back)

# 3.2. Инлайн клавиатуры
startFormMarkup = types.InlineKeyboardMarkup()
confirmFormMarkup = types.InlineKeyboardMarkup()
confirmBookingMarkup = types.InlineKeyboardMarkup()
secondConfirmFormMarkup = types.InlineKeyboardMarkup()

confirmMarkup = types.InlineKeyboardMarkup()

socialMarkup = types.InlineKeyboardMarkup()

# 3.2.1. Соцсети
vk = types.InlineKeyboardButton(text='ВКонтакте', url=get_link('vk'))
inst = types.InlineKeyboardButton(text='Instagram', url=get_link('inst'))
site = types.InlineKeyboardButton(text='Сайт', url=get_link('website'))

socialMarkup.add(vk, inst, site)

# 3.2.3. Анкета
startFormButton = types.InlineKeyboardButton('✏️ Заполнить анкету', callback_data='start')
startFormMarkup.row(startFormButton)

confirmFormButton = types.InlineKeyboardButton('Все правильно👌🏼', callback_data='confirmForm')
confirmFormMarkup.row(confirmFormButton)

confirmBookingButton = types.InlineKeyboardButton('Все правильно👌🏼', callback_data='confirmBooking')
confirmBookingMarkup.row(confirmBookingButton)

# 3.1.2.4. Подтверждение
confirmButton = types.InlineKeyboardButton('✅ Подтвердить', callback_data='confirm')
confirmMarkup.row(confirmButton)