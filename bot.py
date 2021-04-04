# -*- coding: utf-8 -*-

import telebot
import json
import time
from datetime import datetime
from datetime import timedelta
import re
from telebot import types
from threading import Thread
import config
import xlsxwriter
from telebot import apihelper

# Торжественно клянусь однажды сделать этот код хоть капельку более красивым и читабельным.

# 1. Иниализация бота
token = '620961774:AAG8OblnOGEifNP6K2Ekgb7vm07xhGBekaE'
apihelper.proxy = {'https': 'socks5://geek:socks@t.geekclass.ru:7777'}
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

# 2.4. Шаблоны юзеров
defaultUser = {'name': 'name', 'birthday': 'date', 'phone': 'phone',
               'status': 'status', 'username': 'username',
               'confirmed': True, 'confirm_message': None,
               'sending': False, 'edit': False,
               'booking': False, 'rating': False, 'reviewing': False}

user = {'name': '', 'birthday': '', 'phone': '',
        'status': 'guest', 'username': '',
        'confirmed': False, 'confirm_message': None,
        'sending': False, 'edit': False,
        'booking': False, 'rating': False, 'reviewing': False}

# 2.5. Прочее
months = ['января', 'февраля', 'марта',
          'апреля', 'мая', 'июня',
          'июля', 'августа', 'сентября',
          'октября', 'ноября', 'декабря']
rate_messages = {}

# 3. Интерфейс
# 3.1. Юзерский интерфейс
# 3.1.1. Визуальные клавиатуры
hide = types.ReplyKeyboardRemove()
userMarkup = types.ReplyKeyboardMarkup()
menuMarkup = types.ReplyKeyboardMarkup()
reviewMarkup = types.ReplyKeyboardMarkup()
goBackMarkup = types.ReplyKeyboardMarkup()

# 3.1.1.1. Основной функционал
reserve = types.KeyboardButton(smileCalendar)
review = types.KeyboardButton(smilePaper)
menu = types.KeyboardButton(smileBook)
offers = types.KeyboardButton(smileMoney)
social = types.KeyboardButton(smileSocial)
contacts = types.KeyboardButton(smilePhone)
way = types.KeyboardButton(smileMap)
friend = types.KeyboardButton(smileFriend)
back = types.KeyboardButton(goBack)
formEdit = types.KeyboardButton(smileEdit)

userMarkup.row(reserve)
userMarkup.row(menu, offers)
userMarkup.row(social, contacts)
userMarkup.row(way, friend)
userMarkup.row(review)
userMarkup.row(formEdit)

# 3.1.1.2. Меню
hookahMenu = types.KeyboardButton(smileSmoke)
drinksMenu = types.KeyboardButton(smileDrinks)

menuMarkup.row(hookahMenu)
menuMarkup.row(drinksMenu)
menuMarkup.row(back)

# 3.1.1.3. Отзывы
rate = types.KeyboardButton(smileStar)
comment = types.KeyboardButton(smileReview)

reviewMarkup.row(rate)
reviewMarkup.row(comment)
reviewMarkup.row(back)

goBackMarkup.row(back)

# 3.1.2. Инлайн клавиатуры
startFormMarkup = types.InlineKeyboardMarkup()
confirmFormMarkup = types.InlineKeyboardMarkup()
confirmFormEditMarkup = types.InlineKeyboardMarkup()
secondConfirmFormMarkup = types.InlineKeyboardMarkup()

confirmMarkup = types.InlineKeyboardMarkup()

inviteMarkup = types.InlineKeyboardMarkup()
socialMarkup = types.InlineKeyboardMarkup()
rateMarkup = types.InlineKeyboardMarkup()

# 3.1.2.1. Соцсети
vk = types.InlineKeyboardButton(text='ВКонтакте', url='vk.com/nasvyazimsk')
inst = types.InlineKeyboardButton(text='Instagram', url='instagram.com/nasvyazimsk')
site = types.InlineKeyboardButton(text='Сайт', url='nasvyazimsk.ru')

socialMarkup.add(vk, inst, site)

# 3.1.2.2 Оценивание
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

# 3.1.2.3. Анкета
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
friendText = config.friendText
icon = 'https://pp.userapi.com/c840324/v840324996/37de9/dASYxIRQifU.jpg'
friendTextType = types.InputTextMessageContent(message_text=friendText)
inviteFriend = types.InlineQueryResultArticle(id='1', title='Пригласить друга',
                                              description='Нажми, чтобы отправить приглашение',
                                              input_message_content=friendTextType,
                                              thumb_url=icon, thumb_width=48, thumb_height=48)

# 3.2. Интерфейс супер админки
superAdminMarkup = types.ReplyKeyboardMarkup()
posting = types.KeyboardButton(admSend)
getReting = types.KeyboardButton(admRating)
getReviews = types.KeyboardButton(admReviews)
getOut = types.KeyboardButton(admOut)
setPass = types.KeyboardButton(admPass)
getConsumers = types.KeyboardButton(admUsers)

superAdminMarkup.row(posting)
superAdminMarkup.row(getReting, getReviews)
superAdminMarkup.row(getConsumers)
superAdminMarkup.row(setPass)
superAdminMarkup.row(getOut)

# 3.2.1. Изменит пароль
setPassMarkup = types.ReplyKeyboardMarkup()
setAdmPass = types.KeyboardButton(admPassA)
setASuperdmPass = types.KeyboardButton(admPassSA)

setPassMarkup.row(setAdmPass)
setPassMarkup.row(setASuperdmPass)
setPassMarkup.row(back)

# 3.3. Интерфейс админки
adminMarkup = types.ReplyKeyboardMarkup()
adminMarkup.row(getOut)

# 4. Контент
# 4.1. Тексты
helloText = config.helloText
abilitiesText = config.abilitiesText
discountsText = config.discountsText

birthdayText = config.birthdayText

formName = config.formName
formBDay = config.formBDay
formPhone = config.formPhone
formConfirmation = config.formConfirmation
formEdit = config.formEdit
formCheck = config.formCheck
formTryAgain = config.formTryAgain

startFormText = config.startFormText
existUser = config.existUser

bookingRequest = config.bookingRequest
bookingWait = config.bookingWait

networksText = config.networksText
contactsText = config.contactsText

mapText = config.mapText
sendFriendText = config.sendFriendText
rateText = config.rateText
commentText = config.commentText
menuText = config.menuText
reviewText = config.reviewText
formatText = config.formatText

# 4.2. Инфа из JSON
f = open('users.json', 'r')
json_data = f.read()
f.close()
all_data = json.loads(json_data)

users = all_data['users']
birthdays = all_data['birthdays']
password = all_data['password']
superPassword = all_data['super_password']


# 5. Основной код
# 5.1. Обработчики команд пользователя
# 5.1.1. Приветствие
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    bot.send_message(user_id, helloText, reply_markup=hide)
    bot.send_message(user_id, startFormText, reply_markup=startFormMarkup)


# 5.1.2. Анкета
# 5.1.2.1. Первое заполнение и редакция
@bot.message_handler(func=lambda message: all_data['users'].get(str(message.chat.id), defaultUser)['name'] == '' and (
        not all_data['users'].get(str(message.chat.id), defaultUser)['confirmed']) and (
                                                  all_data['users'].get(str(message.chat.id), defaultUser)[
                                                      'confirm_message'] is None))
def get_name(message):
    user_id = message.chat.id
    all_data['users'][str(user_id)]['username'] = message.chat.username
    if re.match("^[А-Яа-я ёЁ]*$", message.text):
        all_data['users'][str(user_id)]['name'] = message.text
        hello = 'Привет, ' + all_data['users'][str(user_id)]['name'] + '!\n' + formBDay
        bot.send_message(user_id, hello, reply_markup=hide)
    else:
        bot.send_message(user_id, formTryAgain + ' Напиши по-русски.', reply_markup=hide)
    write_to_json()


@bot.message_handler(func=lambda message: all_data['users'].get(str(message.chat.id), defaultUser)['name'] == 'editing' and (
        not all_data['users'].get(str(message.chat.id), defaultUser)['confirmed']))
def get_new_name(message):
    user_id = message.chat.id
    text = message.text.split('. ')
    inf = text[len(text)-1]
    if re.match("^[А-Яа-я ёЁ]*$", inf):
        all_data['users'][str(user_id)]['name'] = inf
        write_to_json()
        if all_data['users'][str(user_id)]['edit']:
            edit_confirmation(message)
        else:
            confirmation(message)
    else:
        bot.send_message(user_id, formTryAgain + ' Напиши по-русски.', reply_markup=hide)


@bot.message_handler(func=lambda message: all_data['users'].get(str(message.chat.id), defaultUser)['name'] != '' and (
        all_data['users'].get(str(message.chat.id), defaultUser)['birthday'] == '' and
        not all_data['users'].get(str(message.chat.id), defaultUser)['confirmed']))
def get_birthday(message):
    user_id = message.chat.id
    all_data['users'][str(user_id)]['birthday'] = check_birthday(message, message.text)
    write_to_json()
    if all_data['users'][str(user_id)]['birthday'] != '':
        if all_data['users'][str(user_id)]['birthday'] in all_data['birthdays']:
            all_data['birthdays'][all_data['users'][str(user_id)]['birthday']].append(user_id)
        else:
            all_data['birthdays'].update({all_data['users'][str(user_id)]['birthday']: [user_id]})
        write_to_json()
        bot.send_message(user_id, formPhone)


@bot.message_handler(
    func=lambda message: len(all_data['users'].get(str(message.chat.id), defaultUser)['birthday'].split('*')) > 1 and (
            not all_data['users'].get(str(message.chat.id), defaultUser)['confirmed']))
def get_new_birthday(message):
    user_id = message.chat.id
    text = message.text.split('. ')
    inf = text[len(text)-1]

    buf = all_data['users'].get(str(message.chat.id), defaultUser)['birthday'].split('*')[0]
    all_data['users'][str(user_id)]['birthday'] = check_birthday(message, inf)
    write_to_json()
    if len(all_data['users'][str(user_id)]['birthday'].split('*')) == 1:
        if buf in all_data['birthdays']:
            try:
                all_data['birthdays'][buf].remove(user_id)
            except ValueError:
                pass
            if len(all_data['birthdays'][buf]) == 0:
                all_data['birthdays'].pop(buf, None)
        if all_data['users'][str(user_id)]['birthday'] in all_data['birthdays']:
            all_data['birthdays'][all_data['users'][str(user_id)]['birthday']].append(user_id)
        else:
            all_data['birthdays'].update({all_data['users'][str(user_id)]['birthday']: [user_id]})
        write_to_json()
        if all_data['users'][str(user_id)]['edit']:
            edit_confirmation(message)
        else:
            confirmation(message)


@bot.message_handler(func=lambda message: all_data['users'].get(str(message.chat.id), defaultUser)['birthday'] != '' and (
        all_data['users'].get(str(message.chat.id), defaultUser)['phone'] == '' or
        all_data['users'].get(str(message.chat.id), defaultUser)['phone'] == 'editing') and (
                                                  not all_data['users'].get(str(message.chat.id), defaultUser)['confirmed']))
def get_phone(message):
    user_id = message.chat.id
    text = message.text.split('. ')
    inf = text[len(text)-1]

    all_data['users'][str(user_id)]['phone'] = check_phone(message, inf)
    write_to_json()
    if all_data['users'][str(user_id)]['phone'] != '' and all_data['users'][str(user_id)]['phone'] != 'editing':
        if all_data['users'][str(user_id)]['confirm_message'] is not None:
            if all_data['users'][str(user_id)]['edit']:
                write_to_json()
                edit_confirmation(message)
            else:
                write_to_json()
                confirmation(message)
        else:
            bot.send_message(user_id, formConfirmation, reply_markup=hide)
            information = get_user_information(user_id)
            confirm_message = bot.send_message(user_id, information, reply_markup=confirmFormMarkup)
            all_data['users'][str(user_id)]['confirm_message'] = confirm_message.message_id
            write_to_json()


# 5.1.2.2. Проверка формата ввода
def check_birthday(message, text):
    global months
    user_id = message.chat.id
    try:
        separated_date = text.split(' ')
        separated_date[1] = str(months.index(separated_date[1]) + 1)
        if len(separated_date[1]) == 1:
            separated_date[1] = '0' + separated_date[1]
        if len(separated_date[0]) == 1:
            separated_date[0] = '0' + separated_date[0]
        date = '.'.join(separated_date)
        time.strptime(date, '%d.%m')
        return date
    except Exception:
        try:
            separated_date = text.split('.')
            if len(separated_date[1]) == 1:
                separated_date[1] = '0' + separated_date[1]
            if len(separated_date[0]) == 1:
                separated_date[0] = '0' + separated_date[0]
            date = '.'.join(separated_date)
            time.strptime(date, '%d.%m')
            return date
        except Exception:
            date = all_data['users'][str(user_id)]['birthday']
            bot.send_message(user_id, formTryAgain + '\nЯ не понимаю, что это за дата. ' +
                             'Попробуй в формате dd.mm', reply_markup=hide)
            return date


def check_phone(message, text):
    user_id = message.chat.id
    if re.fullmatch(r'\+?([78])-?\(?\d{3}\)?-?(\d{3})-?(\d{2})-?(\d{2})', text):
        return text
    else:
        bot.send_message(user_id, formTryAgain + '\nЯ таких номеров никогда не видел. Давай в формате 8XXXXXXXXXX',
                         reply_markup=hide)
        return all_data['users'][str(user_id)]['phone']


# 5.1.2.3. Подтверждение анкеты
@bot.message_handler(func=lambda message: all_data['users'].get(str(message.chat.id), defaultUser)['confirm_message'] is not None
                                          and (not all_data['users'].get(str(message.chat.id), defaultUser)['confirmed'] or all_data['users'].get(str(message.chat.id), defaultUser)['edit'])
                                          and message.text != password and message.text != superPassword and message.text != goBack)
def confirm(message):
    global all_data
    user_id = message.chat.id
    edit_command = message.text.split('. ')
    buf = {'birthday': all_data['users'][str(user_id)]['birthday'], 'phone': all_data['users'][str(user_id)]['phone']}

    if len(edit_command) == 2 and edit_command[0] == '1':
        if re.match("^[А-Яа-я ёЁ]*$", edit_command[1]):
            all_data['users'][str(user_id)]['name'] = edit_command[1]
            write_to_json()
            if all_data['users'][str(user_id)]['edit']:
                edit_confirmation(message)
            else:
                confirmation(message)
        else:
            all_data['users'][str(user_id)]['name'] = 'editing'
            bot.send_message(user_id, formTryAgain + ' Напиши по-русски', reply_markup=hide)
    elif len(edit_command) == 2 and edit_command[0] == '2':
        all_data['users'][str(user_id)]['birthday'] = check_birthday(message, edit_command[1])
        if all_data['users'][str(user_id)]['birthday'] == buf['birthday']:
            all_data['users'][str(user_id)]['birthday'] += '*editing'
            write_to_json()
        else:
            if buf['birthday'] in all_data['birthdays']:
                try:
                    all_data['birthdays'][buf['birthday']].remove(user_id)
                except ValueError:
                    pass
                if len(all_data['birthdays'][buf['birthday']]) == 0:
                    all_data['birthdays'].pop(buf['birthday'], None)
            if all_data['users'][str(user_id)]['birthday'] in all_data['birthdays'] and user_id not in all_data['birthdays'][
                all_data['users'][str(user_id)]['birthday']]:
                all_data['birthdays'][all_data['users'][str(user_id)]['birthday']].append(user_id)
            elif all_data['users'][str(user_id)]['birthday'] not in all_data['birthdays']:
                all_data['birthdays'].update({all_data['users'][str(user_id)]['birthday']: [user_id]})
            write_to_json()

            if all_data['users'][str(user_id)]['edit']:
                edit_confirmation(message)
            else:
                confirmation(message)
    elif len(edit_command) == 2 and edit_command[0] == '3':
        all_data['users'][str(user_id)]['phone'] = check_phone(message, edit_command[1])
        if all_data['users'][str(user_id)]['phone'] == buf['phone']:
            all_data['users'][str(user_id)]['phone'] = 'editing'
            write_to_json()
        else:
            write_to_json()
            if all_data['users'][str(user_id)]['edit']:
                edit_confirmation(message)
            else:
                confirmation(message)
    else:
        bot.send_message(user_id, formatText + '\nПроверь, есть ли пробел после точки', reply_markup=hide)
    write_to_json()


def confirmation(message):
    user_id = message.chat.id
    bot.send_message(user_id, formCheck)
    information = get_user_information(user_id)
    bot.edit_message_text(information, chat_id=user_id,
                          message_id=all_data['users'][str(user_id)]['confirm_message'],
                          reply_markup=confirmFormMarkup)


def get_user_information(user_id):
    try:
        return '1. Тебя зовут ' + all_data['users'][str(user_id)]['name'] \
               + '\n2. Твой День рождения ' + all_data['users'][str(user_id)]['birthday'] \
               + '\n3. Номер ' + all_data['users'][str(user_id)]['phone']
    except Exception:
        return '1Тебя зовут ' + all_data['users'][str(user_id)]['name'] \
               + '\n2. Твой День рождения ' + all_data['users'][str(user_id)]['birthday'] \
               + '\n3. Номер ' + all_data['users'][str(user_id)]['phone']


# 5.1.2.4. Редактировать анкету
@bot.message_handler(func=lambda message: message.text == smileEdit and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'guest'))
def edit_form(message):
    user_id = message.chat.id
    bot.send_message(user_id, formEdit, reply_markup=goBackMarkup)
    information = get_user_information(user_id)
    confirm_message = bot.send_message(user_id, information, reply_markup=confirmFormEditMarkup)
    all_data['users'][str(user_id)]['confirm_message'] = confirm_message.message_id
    all_data['users'][str(user_id)]['confirmed'] = False
    all_data['users'][str(user_id)]['edit'] = True
    write_to_json()


def edit_confirmation(message):
    user_id = message.chat.id
    bot.send_message(user_id, formCheck)
    information = get_user_information(user_id)
    bot.edit_message_text(information, chat_id=user_id,
                          message_id=all_data['users'][str(user_id)]['confirm_message'],
                          reply_markup=confirmFormEditMarkup)


# 5.1.3 Забронировать стол
@bot.message_handler(func=lambda message: message.text == smileCalendar and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'guest'))
def book_table(message):
    user_id = message.chat.id
    bot.send_message(user_id, bookingRequest, reply_markup=goBackMarkup)
    all_data['users'][str(user_id)]['booking'] = True
    write_to_json()


@bot.message_handler(func=lambda message: all_data['users'].get(str(message.chat.id), defaultUser)['booking'] and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'guest') and message.text != goBack)
def book_table_wait(message):
    user_id = message.chat.id
    message_text = message.text.replace("*", "")
    info = '*Бронь.*\n*Имя из анкеты:* ' + all_data['users'][str(user_id)]['name'] \
           + '\n*Номер из анкеты:* ' + all_data['users'][str(user_id)]['phone'] \
           + '\n*Логин в телеге:* @' + message.chat.username \
           + '\n*Сообщение:*\n' + message_text
    messages = {}
    for _id in all_data['admins']:
        try:
            m = bot.send_message(_id, info,
                                 parse_mode='Markdown', reply_markup=confirmMarkup)
            messages.update({str(_id): m.message_id})
        except:
            pass

    all_data['book'].update({message.chat.username: messages})
    write_to_json()

    bot.send_message(user_id, bookingWait, reply_markup=userMarkup)
    all_data['users'][str(user_id)]['booking'] = False
    write_to_json()


# 5.1.4. Наше меню
@bot.message_handler(func=lambda message: message.text == smileBook and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'guest'))
def show_menu(message):
    bot.send_message(message.chat.id, menuText, reply_markup=menuMarkup)


@bot.message_handler(func=lambda message: message.text == smileDrinks and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'guest'))
def drinks_menu(message):
    bot.send_message(message.chat.id, 'goo.gl/FzeKBa', reply_markup=userMarkup)


@bot.message_handler(func=lambda message: message.text == smileSmoke and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'guest'))
def hookah_menu(message):
    bot.send_message(message.chat.id, 'goo.gl/rhqu8T', reply_markup=userMarkup)


# 5.1.5. Лови акции
@bot.message_handler(func=lambda message: message.text == smileMoney and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'guest'))
def show_discounts(message):
    bot.send_message(message.chat.id, discountsText, reply_markup=userMarkup)


# 5.1.6. Лови соцсети
@bot.message_handler(func=lambda message: message.text == smileSocial and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'guest'))
def show_networks(message):
    bot.send_message(message.chat.id, networksText, reply_markup=socialMarkup)


# 5.1.7. Контакты
@bot.message_handler(func=lambda message: message.text == smilePhone and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'guest'))
def show_networks(message):
    bot.send_message(message.chat.id, contactsText, reply_markup=userMarkup)


# 5.1.8. Дорогу покажи
@bot.message_handler(func=lambda message: message.text == smileMap and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'guest'))
def show_way(message):
    bot.send_message(message.chat.id, mapText, reply_markup=userMarkup)
    bot.send_location(message.chat.id, 55.757632, 37.633183, reply_markup=userMarkup)


# 5.1.9. Позови друга
@bot.message_handler(func=lambda message: message.text == smileFriend and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'guest'))
def call_friend(message):
    bot.send_message(message.chat.id, sendFriendText, reply_markup=inviteMarkup)


@bot.inline_handler(func=lambda query: len(query.query) > -1)
def invite_friend(query):
    bot.answer_inline_query(query.id, [inviteFriend])


# 5.1.10. Написать администрации
@bot.message_handler(func=lambda message: message.text == smilePaper and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'guest'))
def reviewing(message):
    bot.send_message(message.chat.id, reviewText, reply_markup=reviewMarkup)


# 5.1.10.1. Оценка
@bot.message_handler(func=lambda message: message.text == smileStar and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'guest'))
def choose_rate(message):
    m = bot.send_message(message.chat.id, rateText, reply_markup=rateMarkup)
    rate_messages.update({message.chat.id: m})
    all_data['users'][str(message.chat.id)]['rating'] = True
    write_to_json()


@bot.message_handler(func=lambda message: all_data['users'].get(str(message.chat.id), defaultUser)['rating'] and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'guest'))
def get_rate(message):
    user_id = message.chat.id
    try:
        if 0 <= float(message.text) <= 10:
            all_data['users'][str(user_id)]['rating'] = False
            all_data['rates'].append(float(message.text))
            write_to_json()

            bot.edit_message_reply_markup(user_id, rate_messages[user_id].message_id, reply_markup=None)
            try:
                rate_messages.pop(user_id, None)
            except Exception:
                pass

            for _id in all_data['admins']:
                if all_data['users'][str(_id)]['status'] == 'superadmin':
                    try:
                        bot.send_message(_id, '*Новая оценка:* ' + message.text + ' от @' + message.chat.username,
                                     parse_mode='Markdown', reply_markup=superAdminMarkup)
                    except:
                        pass
            bot.send_message(user_id, 'Спасибо за оценку!', reply_markup=userMarkup)
    except Exception:
        bot.send_message(user_id, formatText, reply_markup=hide)


# 5.1.10.2. Отзыв
@bot.message_handler(func=lambda message: message.text == smileReview and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'guest'))
def send_review(message):
    bot.send_message(message.chat.id, commentText, reply_markup=goBackMarkup)
    all_data['users'][str(message.chat.id)]['reviewing'] = True
    write_to_json()


@bot.message_handler(func=lambda message: all_data['users'].get(str(message.chat.id), defaultUser)['reviewing'] and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'guest') and message.text != goBack)
def get_review(message):
    user_id = message.chat.id
    all_data['users'][str(user_id)]['reviewing'] = False

    all_data['reviews'].append(message.text)
    bot.send_message(user_id, 'Спасибо за отзыв!', reply_markup=userMarkup)
    write_to_json()

    for _id in all_data['admins']:
        if all_data['users'][str(_id)]['status'] == 'superadmin':
            try:
                message_text = message.text.replace("*","")
                bot.send_message(_id, '*Анонимка*\n' + message.text,
                             parse_mode='Markdown', reply_markup=superAdminMarkup)
            except:
                pass


# 5.2 Обработчики команд админа
# 5.2.1 Проверка пароля
@bot.message_handler(func=lambda message: message.text == password)
def check_adm(message):
    global all_data
    user_id = message.chat.id

    if str(user_id) not in all_data['users']:
        user_dict = {str(user_id): user}
        user_dict[str(user_id)]['status'] = 'admin'
        user_dict[str(user_id)]['confirmed'] = True
        user_dict[str(user_id)]['username'] = message.chat.username
        all_data['users'].update(user_dict)
    else:
        all_data['users'][str(user_id)]['username'] = message.chat.username
        all_data['users'][str(user_id)]['status'] = 'admin'
        all_data['users'][str(user_id)]['confirmed'] = True

    if user_id not in all_data['admins']:
        all_data['admins'].append(user_id)
    write_to_json()
    bot.send_message(user_id, 'Вы зашли в режим админки', reply_markup=adminMarkup)


# 5.2.2. Рассылка
@bot.message_handler(func=lambda message: message.text == admSend and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'admin' or
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'superadmin'))
def sending_to_guests(message):
    bot.send_message(message.chat.id, 'Напишите текст рассылки', reply_markup=goBackMarkup)
    all_data['users'][str(message.chat.id)]['sending'] = True
    write_to_json()


@bot.message_handler(func=lambda message: all_data['users'].get(str(message.chat.id), defaultUser)['sending'] and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'admin' or
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'superadmin') and message.text != goBack)
def send_to_guests(message):
    for _id in all_data['users'].keys():
        if all_data['users'][_id]['status'] == 'guest' and all_data['users'][_id]['confirmed']:
            try:
                bot.send_message(_id, message.text)
            except:
                pass
    if all_data['users'][str(message.chat.id)]['status'] == 'superadmin':
        bot.send_message(message.chat.id, 'Готово', reply_markup=superAdminMarkup)
    else:
        bot.send_message(message.chat.id, 'Готово', reply_markup=adminMarkup)
    all_data['users'][str(message.chat.id)]['sending'] = False
    write_to_json()


# 5.3. Обработчики команд супер-админа
# 5.3.1. Проверка пароля
@bot.message_handler(func=lambda message: message.text == superPassword)
def check_superadm(message):
    user_id = message.chat.id

    if str(user_id) not in all_data['users']:
        user_dict = {str(user_id): user}
        user_dict[str(user_id)]['username'] = message.chat.username
        user_dict[str(user_id)]['status'] = 'superadmin'
        user_dict[str(user_id)]['confirmed'] = True
        all_data['users'].update(user_dict)
    else:
        all_data['users'][str(user_id)]['username'] = message.chat.username
        all_data['users'][str(user_id)]['status'] = 'superadmin'
        all_data['users'][str(user_id)]['confirmed'] = True
    if user_id not in all_data['admins']:
        all_data['admins'].append(user_id)
    write_to_json()

    bot.send_message(user_id, 'Вы зашли в режим супер админки', reply_markup=superAdminMarkup)


# 5.3.2. Получить рейтинг
@bot.message_handler(func=lambda message: message.text == admRating and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'superadmin'))
def get_rating(message):
    rating = 0
    _min = 11
    _max = 0
    for i in all_data['rates']:
        rating += i
        if i < _min:
            _min = i
        if i > _max:
            _max = i
    try:
        rating /= len(all_data['rates'])
        info = '*Средний рейтинг:* ' + str(round(rating, 2)) + '\n' + '*Самая низкая оценка:* ' + str(
            _min) + '\n' + '*Самая высокая оценка:* ' + str(_max) + '\n' + '*Всего оценок:* ' + str(len(all_data['rates']))
        bot.send_message(message.chat.id, info, reply_markup=superAdminMarkup, parse_mode='Markdown')
    except ZeroDivisionError:
        bot.send_message(message.chat.id, 'Никто еще не ставил оценки', reply_markup=superAdminMarkup)


# 5.3.2. Получить клиентскую базу
@bot.message_handler(func=lambda message: message.text == admUsers and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'superadmin'))
def get_consumers(message):
    workbook = xlsxwriter.Workbook('Consumers.xlsx')
    worksheet = workbook.add_worksheet()
    title_format = workbook.add_format({'bold': True, 'font_size': 12, 'font_name': 'Bangla Sangam MN', 'align': 'center', 'valign': 'center', 'bg_color': '#8FC3E5', 'text_wrap': True})
    cell_format = workbook.add_format({'font_size': 12, 'font_name': 'Bangla Sangam MN', 'align': 'center', 'valign': 'center', 'text_wrap': True})
    row = 0
    col = 0
    
    worksheet.write(row, col, 'Имя', title_format)
    worksheet.write(row, col + 1, 'День Рождения', title_format)
    worksheet.write(row, col + 2, 'Номер телефона', title_format)
    worksheet.write(row, col + 3, 'Аккаунт', title_format)
    row += 1

    for consumer in all_data['users']:
        if all_data['users'][consumer]['status'] == 'guest' and all_data['users'][consumer]['username'] != None and all_data['users'][consumer]['confirmed']:
            worksheet.write(row, col, all_data['users'][consumer]['name'], cell_format)
            worksheet.write(row, col + 1, all_data['users'][consumer]['birthday'], cell_format)
            worksheet.write(row, col + 2, all_data['users'][consumer]['phone'], cell_format)
            worksheet.write(row, col + 3, '@'+all_data['users'][consumer]['username'], cell_format)
            row += 1

    workbook.close()
    consumers = open('Consumers.xlsx', 'rb')
    bot.send_document(message.chat.id, consumers, reply_markup=superAdminMarkup)
    consumers.close()
    workbook = xlsxwriter.Workbook('Consumers.xlsx')
    worksheet = workbook.add_worksheet()
    workbook.close()


# 5.3.2. Почитать отзыв
@bot.message_handler(func=lambda message: message.text == admReviews and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'superadmin'))
def get_consumers(message):
    text = 'Отзывы\n'
    i = 1
    for review in all_data['reviews']:
        text+=str(i)+'. ' + review + '\n'
        i += 1
    f = open('reviews.txt', 'w')
    f.write(text)
    f.close()
    reviews = open('reviews.txt', 'rb')
    bot.send_document(message.chat.id, reviews, reply_markup=superAdminMarkup)
    reviews.close()


# 5.3.4. Изменит пароль
@bot.message_handler(func=lambda message: message.text == admPass and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'superadmin'))
def set_pass(message):
    bot.send_message(message.chat.id, 'Какой пароль изменить?', reply_markup=setPassMarkup)


@bot.message_handler(func=lambda message: (message.text == admPassA or
                                           message.text == admPassSA) and (
                                                  all_data['users'].get(str(message.chat.id), defaultUser)[
                                                      'status'] == 'superadmin'))
def set_adm_pass(message):
    all_data['users'][str(message.chat.id)]['edit'] = True
    if message.text == admPassA:
        all_data['password'] = 'editing'
    else:
        all_data['super_password'] = 'editing'
    write_to_json()
    bot.send_message(message.chat.id, 'Напишите новый пароль', reply_markup=goBackMarkup)


@bot.message_handler(func=lambda message: all_data['users'].get(str(message.chat.id), defaultUser)['edit'] and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'superadmin') and message.text != goBack)
def set_adm_pass(message):
    global password, superPassword
    all_data['users'][str(message.chat.id)]['edit'] = False
    if all_data['password'] == 'editing':
        all_data['password'] = message.text
        password = all_data['password']
    elif all_data['super_password'] == 'editing':
        all_data['super_password'] = message.text
        superPassword = all_data['super_password']
    write_to_json()
    bot.send_message(message.chat.id, 'Готово', reply_markup=superAdminMarkup)


# 5.3.5. Выйти из админки
@bot.message_handler(func=lambda message: message.text == admOut and (
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'admin' or
        all_data['users'].get(str(message.chat.id), defaultUser)['status'] == 'superadmin'))
def get_out_adm(message):
    all_data['users'][str(message.chat.id)]['status'] = 'guest'
    if all_data['users'][str(message.chat.id)]['name'] == '':
        all_data['users'][str(message.chat.id)]['confirmed'] = False
        bot.send_message(message.chat.id, 'Вы вышли из режима админки.', reply_markup=hide)
        bot.send_message(message.chat.id, formName)
    else:
        bot.send_message(message.chat.id, 'Вы вышли из режима админки.', reply_markup=userMarkup)
    try:
        all_data['admins'].remove(message.chat.id)
    except ValueError:
        pass
    write_to_json()


# 5.4. Назад в меню
@bot.message_handler(func=lambda message: message.text == goBack)
def response_for_mess(message):
    user_id = message.chat.id
    all_data['users'][str(user_id)]['rating'] = False
    all_data['users'][str(user_id)]['reviewing'] = False
    all_data['users'][str(user_id)]['booking'] = False
    all_data['users'][str(user_id)]['edit'] = False
    all_data['users'][str(user_id)]['sending'] = False
    try:
        bot.edit_message_reply_markup(user_id, all_data['users'][str(user_id)]['confirm_message'], reply_markup=None)
    except Exception:
        pass
    all_data['users'][str(user_id)]['confirm_message'] = None
    write_to_json()
    if all_data['users'][str(user_id)]['status'] == 'guest':
        bot.send_message(user_id, 'Ок', reply_markup=userMarkup)
    elif all_data['users'][str(user_id)]['status'] == 'admin':
        bot.send_message(user_id, 'Ок', reply_markup=adminMarkup)
    if all_data['users'][str(user_id)]['status'] == 'superadmin':
        bot.send_message(user_id, 'Ок', reply_markup=superAdminMarkup)


# 5.5. Ответ на непонятные сообщения
@bot.message_handler(content_types=['text'])
def response_for_mess(message):
    user_id = message.chat.id
    if str(user_id) not in all_data['users'].keys():
        bot.send_message(user_id, 'Сначала заполни анкету до конца 😉')
        return 0
    if all_data['users'][str(user_id)]['status'] == 'guest' and all_data['users'][str(user_id)]['confirmed']:
        if all_data['users'][str(user_id)]['booking'] or all_data['users'][str(user_id)]['rating'] or \
                all_data['users'][str(user_id)]['reviewing']:
            bot.send_message(user_id, 'Я не понимаю(\nДавай еще раз.', reply_markup=userMarkup)
        else:
            bot.send_message(user_id, 'Я не понимаю ¯\_(ツ)_/¯\nИспользуй кнопки', reply_markup=userMarkup)
    elif all_data['users'][str(user_id)]['status'] == 'admin':
        bot.send_message(user_id, 'Я не понимаю', reply_markup=adminMarkup)
    elif all_data['users'][str(user_id)]['status'] == 'superadmin':
        bot.send_message(user_id, 'Я не понимаю.', reply_markup=superAdminMarkup)
    else:
        bot.send_message(user_id, 'Сначала заполни анкету до конца 😉')


# 5.5. КоллБэк
@bot.callback_query_handler(func=lambda call: True)
def callback_confirm(call):
    global all_data, password, superPassword
    user_id = call.message.chat.id
    try:
        call_username = all_data['users'][str(user_id)]['username']
    except:
        try:
            call_username = call.message.chat.username
        except:
            call_username = '[NO_USERNAME]'
    try:
        bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)
    except Exception:
        pass

    if call.data == 'start':
        if str(user_id) in all_data['users']:
            all_data['users'][str(user_id)]['rating'] = False
            all_data['users'][str(user_id)]['sending'] = False
            all_data['users'][str(user_id)]['edit'] = False
            all_data['users'][str(user_id)]['reviewing'] = False
            all_data['users'][str(user_id)]['booking'] = False
            
            if all_data['users'][str(user_id)]['confirmed']:
                all_data['users'][str(user_id)]['confirm_message'] = None
                all_data['users'][str(user_id)]['confirmed'] = False
                text = existUser + all_data['users'][str(user_id)]['name'] + '?'
                write_to_json()
                bot.send_message(user_id, text, reply_markup=secondConfirmFormMarkup)
                return
            else:
                if all_data['users'][str(user_id)]['birthday'] in all_data['birthdays']:
                    try:
                        all_data['birthdays'][all_data['users'][str(user_id)]['birthday']].remove(user_id)
                    except ValueError:
                        pass
                    if len(all_data['birthdays'][all_data['users'][str(user_id)]['birthday']]) == 0:
                        all_data['birthdays'].pop(all_data['users'][str(user_id)]['birthday'], None)
                all_data['users'].pop(str(user_id), None)
        user = {'name': '', 'birthday': '', 'phone': '',
                'status': 'guest', 'username': '',
                'confirmed': False, 'confirm_message': None,
                'sending': False, 'edit': False,
                'booking': False, 'rating': False, 'reviewing': False}
        user_dict = {str(user_id): user}
        all_data['users'].update(user_dict)
        bot.send_message(user_id, formName, reply_markup=hide)

    elif call.data == 'confirmFormEdit':
        all_data['users'][str(user_id)]['confirmed'] = True
        all_data['users'][str(user_id)]['edit'] = False
        all_data['users'][str(user_id)]['confirm_message'] = None
        bot.send_message(user_id, 'Готово', reply_markup=userMarkup)

    elif call.data == 'confirmForm':
        all_data['users'][str(user_id)]['confirmed'] = True
        all_data['users'][str(user_id)]['confirm_message'] = None
        bot.send_message(user_id, abilitiesText, reply_markup=userMarkup)

    elif call.data == 'notMe':
        if all_data['users'][str(user_id)]['birthday'] in all_data['birthdays']:
            try:
                all_data['birthdays'][all_data['users'][str(user_id)]['birthday']].remove(user_id)
            except ValueError:
                pass
            if len(all_data['birthdays'][all_data['users'][str(user_id)]['birthday']]) == 0:
                all_data['birthdays'].pop(all_data['users'][str(user_id)]['birthday'], None)
        bot.send_message(user_id, 'Тогда заполним новую анкету!\n' + formName, reply_markup=hide)
        user = {'name': '', 'birthday': '', 'phone': '',
                'status': 'guest', 'username': '',
                'confirmed': False, 'confirm_message': None,
                'sending': False, 'edit': False,
                'booking': False, 'rating': False, 'reviewing': False}
        user_dict = {str(user_id): user}
        all_data['users'].update(user_dict)
        all_data['users'][str(user_id)]['username'] = call_username

    elif call.data == 'me':
        bot.send_message(user_id, formConfirmation)
        information = get_user_information(user_id)
        confirm_message = bot.send_message(user_id, information, reply_markup=confirmFormMarkup)
        all_data['users'][str(user_id)]['confirm_message'] = confirm_message.message_id
        all_data['users'][str(user_id)]['confirmed'] = False

    elif call.data == 'confirm':
        username = call.message.text.split('@')[1]
        username = username.split('\n')[0]
        confirm_time = datetime.now()
        confirm_time += timedelta(hours=8)
        try:
            info = '*Подтверждено @' + call_username + ' в ' + confirm_time.strftime('%H:%M') + '*\n' + call.message.text
        except:
            info = '*Подтверждено*\n' + call.message.text
        for book_message in all_data['book'][username].keys():
            bot.edit_message_text(info, chat_id=int(book_message), parse_mode='Markdown',
                                  message_id=all_data['book'][username][book_message])
            if all_data['book'][username][book_message] != call.message.message_id:
                try:
                    bot.edit_message_reply_markup(user_id, all_data['book'][username][book_message], reply_markup=adminMarkup)
                except Exception:
                        pass
        bot.send_message(user_id, 'Готово! Другие администраторы оповещены', reply_markup=adminMarkup)
        if username in all_data['book']:
            all_data['book'].pop(username, None)
    else:
        all_data['users'][str(user_id)]['rating'] = False
        all_data['rates'].append(float(call.data))

        for _id in all_data['admins']:
            if all_data['users'][str(_id)]['status'] == 'superadmin':
                try:
                    bot.send_message(_id, '*Новая оценка:* ' + call.data + ' от @' + call.message.chat.username,
                                 parse_mode='Markdown', reply_markup=superAdminMarkup)
                except:
                    pass
        bot.edit_message_text('Спасибо за оценку!', chat_id=user_id, message_id=call.message.message_id)
    write_to_json()


# 5.6. Работа с JSON
def read_json():
    global f, json_data, all_data
    f = open('users.json', 'r')
    json_data = f.read()
    f.close()
    all_data = json.loads(json_data)


def write_to_json():
    global json_data, f, all_data
    json_data = json.dumps(all_data, indent=6,  ensure_ascii=False)
    f = open("users.json", 'w')
    f.write(json_data)
    f.close()


# 5.7. Постоянный polling и проверка на день рождения
def birthday_congrats():
    while True:
        now = datetime.now() + timedelta(hours=8)
        if now.hour == 12:
            if now.strftime('%d.%m') in all_data['birthdays']:
                for _id in all_data['birthdays'][now.strftime('%d.%m')]:
                    try:
                        bot.send_message(_id, birthdayText)
                    except:
                        pass
        time.sleep(60 * 60)



while True:
    try:
        bot.polling(none_stop=True, timeout=123)
    except Exception as e:
        time.sleep(5)

if __name__ == '__main__':
    thread_bday = Thread(target=birthday_congrats)
    thread_bday.start()
