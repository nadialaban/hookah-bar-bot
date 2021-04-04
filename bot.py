from db_manager import *

import telebot
from telebot import types
from telebot import apihelper

# 1. Иниализация бота
apihelper.proxy = {'https': proxy}
bot = telebot.TeleBot(token)

# 2. Константы
# 2.1. Юзерские кнопки
smileSmoke = '💨 Меню кальянов'
smileDrinks = '☕️ Меню напитков'

smileCalendar = '📆 Забронировать стол'
smilePaper = '📨 Написать нам'
smileBook = '📕 Меню'
smileMoney = '💸 Акции и скидки'
smileSocial = '👥 Социальные сети'
smilePhone = '📱 Контакты'
smileMap = '🚖 Как добраться'
smileFriend = '🤙 Позови друга'
smileStar = '⭐️ Оценить качество обслуживания'
smileReview = '✉️ Написать анонимно'
smileEdit = '📝 Редактировать анкету'
goBack = '↩️ Вернуться назад'

# 2.2. Админские кнопки
admSend = '📨 Сделать рассылку'

# 2.3. СуперАдминские кнопки
admRating = '⭐️ Получить рейтинг'
admReviews = '📑 Почитать отзывы'
admUsers = '👥 Посмотреть список гостей'
admOut = '✖️ Выйти из админки'
admPass = '🔐 Установить пароль'
admPassA = '👨🏻 Админка'
admPassSA = '🤴🏻 Супер админка'

# 3. Интерфейс
# 3.1. Визуальные клавиатуры
hide = types.ReplyKeyboardRemove()

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
        Как добраться - поделиться
        Оценить
        Редактировать анкету
'''
userMarkup.row(types.KeyboardButton(smileCalendar))
userMarkup.row(types.KeyboardButton(smileBook), types.KeyboardButton(smileMoney))
userMarkup.row(types.KeyboardButton(smileSocial), types.KeyboardButton(smilePhone))
userMarkup.row(types.KeyboardButton(smileMap), types.KeyboardButton(smileFriend))
userMarkup.row(types.KeyboardButton(smilePaper))
userMarkup.row(types.KeyboardButton(smileEdit))

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

# 3.1.1.3. Оценить качество обслужениания
'''
Структура:
        Оценка по 10баьной шкале
        Отзыв
        назад
'''
reviewMarkup.row(types.KeyboardButton(smileStar))
reviewMarkup.row(types.KeyboardButton(smileReview))
reviewMarkup.row(back)

# 3.1.2. Интерфейс супер админки
# 3.1.2.1. Основной функционал
'''
Структура главного меню админа:
        Рассылка
        Рейтинг - Отзывы
        Пользователи
'''
superAdminMarkup = types.ReplyKeyboardMarkup()

superAdminMarkup.row(types.KeyboardButton(admSend))
superAdminMarkup.row(types.KeyboardButton(admRating), types.KeyboardButton(admReviews))
superAdminMarkup.row(types.KeyboardButton(admUsers))

# 3.2. Инлайн клавиатуры
startFormMarkup = types.InlineKeyboardMarkup()
confirmFormMarkup = types.InlineKeyboardMarkup()
confirmFormEditMarkup = types.InlineKeyboardMarkup()
secondConfirmFormMarkup = types.InlineKeyboardMarkup()

confirmMarkup = types.InlineKeyboardMarkup()

inviteMarkup = types.InlineKeyboardMarkup()
socialMarkup = types.InlineKeyboardMarkup()
rateMarkup = types.InlineKeyboardMarkup()

# 3.2.1. Соцсети
vk = types.InlineKeyboardButton(text='ВКонтакте', url=get_message('vk'))
inst = types.InlineKeyboardButton(text='Instagram', url=get_message('inst'))
site = types.InlineKeyboardButton(text='Сайт', url=get_message('website'))

socialMarkup.add(vk, inst, site)

# 3.2.2 Оценивание
r1 = types.InlineKeyboardButton('1 ⭐️', callback_data='1')
r2 = types.InlineKeyboardButton('2 ⭐️', callback_data='2')
r3 = types.InlineKeyboardButton('3 ⭐️', callback_data='3')
r4 = types.InlineKeyboardButton('4 ⭐️', callback_data='4')
r5 = types.InlineKeyboardButton('5 ⭐️', callback_data='5')
r6 = types.InlineKeyboardButton('6 ⭐️', callback_data='6')
r7 = types.InlineKeyboardButton('7 ⭐️', callback_data='7')
r8 = types.InlineKeyboardButton('8 ⭐️', callback_data='8')
r9 = types.InlineKeyboardButton('9 ⭐️', callback_data='9')
r10 = types.InlineKeyboardButton('10 ⭐️', callback_data='10')

rateMarkup.row(r1, r2, r3, r4, r5)
rateMarkup.row(r6, r7, r8, r9, r10)

# 3.2.3. Анкета
startFormButton = types.InlineKeyboardButton('✏️ Заполнить анкету', callback_data='start')
startFormMarkup.row(startFormButton)

confirmFormButton = types.InlineKeyboardButton('Все правильно👌🏼', callback_data='confirmForm')
confirmFormMarkup.row(confirmFormButton)

confirmFormEditButton = types.InlineKeyboardButton('Все правильно 👌🏼', callback_data='confirmFormEdit')
confirmFormEditMarkup.row(confirmFormEditButton)

notMeButton = types.InlineKeyboardButton('❌ Это не я', callback_data='notMe')
meButton = types.InlineKeyboardButton('✅ Это я', callback_data='me')
secondConfirmFormMarkup.row(meButton, notMeButton)

# 3.1.2.4. Подтверждение
confirmButton = types.InlineKeyboardButton('✅ Подтвердить', callback_data='confirm')
confirmMarkup.row(confirmButton)

# 3.1.2.5. Пригласить друга
inviteButton = types.InlineKeyboardButton('📨 Пригласить', switch_inline_query='')
inviteMarkup.row(inviteButton)

# 3.1.3. Инлайн вызов в чате
friendTextType = types.InputTextMessageContent(message_text=get_message('share'))
inviteFriend = types.InlineQueryResultArticle(id='1', title='Пригласить друга',
                                              description='Нажми, чтобы отправить приглашение',
                                              input_message_content=friendTextType,
                                              thumb_url=get_message('logo'), thumb_width=48, thumb_height=48)

