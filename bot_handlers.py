from bot import *
import re
from datetime import datetime


# 0. Назад
@bot.message_handler(func=lambda message: message.text == goBack)
def response_for_mess(message):
    chat_id = message.chat.id
    set_user_state(chat_id, None)

    bot.send_message(chat_id, 'Ок', reply_markup=userMarkup)


# 1. Обработчики команд пользователя
# 1.1. Приветствие
@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    add_user(chat_id)

    bot.send_message(chat_id, get_message('greeting'), reply_markup=hide)
    confirm_message = bot.send_message(chat_id, get_message('startForm'), reply_markup=startFormMarkup)
    set_user_data(chat_id, 'confirm_message', confirm_message.message_id)


# 1.2. Анкета
# 1.2.1. Имя
@bot.message_handler(func=lambda message: check_user_state(message.chat.id, 'get_name'))
def get_name(message):
    chat_id = message.chat.id

    if re.match("^[А-Яа-я ёЁ-]+$", message.text):
        set_user_data(chat_id, 'name', message.text)
        set_user_state(chat_id, 'get_phone')
        bot.send_message(chat_id, 'Привет, {}!\n{}'.format(message.text, get_message('formPhone')), reply_markup=hide)
    else:
        bot.send_message(chat_id, get_message('wrongNameFormat'))


# 1.2.2. Номер телефона
@bot.message_handler(func=lambda message: check_user_state(message.chat.id, 'get_phone'))
def get_phone(message):
    chat_id = message.chat.id

    if re.match("^\+7 (\d{3}) (\d{3})-(\d{2})-(\d{2})$", message.text):
        set_user_data(chat_id, 'phone', message.text)
        set_user_state(chat_id, 'edit')

        bot.send_message(chat_id, get_message('formConfirmation'))
        confirm_message = bot.send_message(chat_id, get_user_info(chat_id), reply_markup=confirmFormMarkup)
        set_user_data(chat_id, 'confirm_message', confirm_message.message_id)
    else:
        bot.send_message(chat_id, get_message('wrongPhoneFormat'))


# 1.2.3. Редактирование формы
@bot.message_handler(func=lambda message: check_user_state(message.chat.id, 'edit'))
def edit_form(message):
    chat_id = message.chat.id

    if not re.match("^[12]\. .+$", message.text):
        bot.send_message(chat_id, get_message('wrongFormat'))
        return

    if message.text[0] == '1':
        if re.match("^[А-Яа-я ёЁ]*$", message.text[3:]):
            set_user_data(chat_id, 'name', message.text[3:])
            edit_confirmation(chat_id)
        else:
            bot.send_message(chat_id, get_message('wrongNameFormat'))

    elif message.text[0] == '2':
        if re.match("^\+7 (\d{3}) (\d{3})-(\d{2})-(\d{2})$", message.text[3:]):
            set_user_data(chat_id, 'phone', message.text[3:])
            edit_confirmation(chat_id)
        else:
            bot.send_message(chat_id, get_message('wrongPhoneFormat'))


# 1.2.4. Номер телефона
@bot.message_handler(func=lambda message: check_user_state(message.chat.id, 'get_code'))
def get_code(message):
    chat_id = message.chat.id

    if re.match("^\d{4}$", message.text):
        res = post('/auth/confirm-number', {
            "userId": get_user_data(chat_id, 'userId'),
            "code": message.text,
        })
        if res['status'] == 'SUCCESS':
            bot.send_message(chat_id, 'Номер телефона успешно подтвержден!')
            bot.send_message(chat_id, get_message('abilities'), reply_markup=userMarkup)
            clear_user_data(chat_id)
        else:
            bot.send_message(chat_id, 'Неверный код. Попробуйте снова')
    else:
        bot.send_message(chat_id, 'Код - это 4 цифры, которые пришли по СМС')


# 1.3. Информация о заведении
# 1.3.1. Меню
@bot.message_handler(func=lambda message: message.text == smileBook)
def show_menu(message):
    bot.send_message(message.chat.id, get_message('menu'), reply_markup=menuMarkup)


@bot.message_handler(func=lambda message: message.text == smileDrinks)
def drinks_menu(message):
    bot.send_message(message.chat.id, 'goo.gl/FzeKBa', reply_markup=userMarkup)


@bot.message_handler(func=lambda message: message.text == smileSmoke)
def hookah_menu(message):
    bot.send_message(message.chat.id, 'goo.gl/rhqu8T', reply_markup=userMarkup)


# 1.3.2. Акции
@bot.message_handler(func=lambda message: message.text == smileMoney)
def show_discounts(message):
    bot.send_message(message.chat.id, get_message('discounts'), reply_markup=userMarkup)


# 1.3.3. Соцсети
@bot.message_handler(func=lambda message: message.text == smileSocial)
def show_networks(message):
    bot.send_message(message.chat.id, get_message('networks'), reply_markup=socialMarkup)


# 1.3.4. Контакты
@bot.message_handler(func=lambda message: message.text == smilePhone)
def show_networks(message):
    bot.send_message(message.chat.id, get_message('contacts'), reply_markup=userMarkup)


# 1.3.5. Как добраться
@bot.message_handler(func=lambda message: message.text == smileMap)
def show_way(message):
    bot.send_message(message.chat.id, get_message('map'), reply_markup=userMarkup)
    bot.send_location(message.chat.id, 55.757632, 37.633183, reply_markup=userMarkup)


# 1.4. Бронирование
# 1.4.1. Начало
@bot.message_handler(func=lambda message: message.text == smileCalendar)
def start_booking(message):
    chat_id = message.chat.id
    set_user_state(chat_id, 'booking_date')
    bot.send_message(chat_id, get_message('book'), reply_markup=goBackMarkup)


# 1.4.2. Дата
@bot.message_handler(func=lambda message: check_user_state(message.chat.id, 'booking_date'))
def get_booking_date(message):
    chat_id = message.chat.id

    try:
        date = datetime.strptime(message.text, '%d.%m.%Y %H:%M')
        set_user_data(chat_id, 'timeFrom', date.strftime('%Y-%m-%dT%H:00:00.000Z'))
        set_user_data(chat_id, 'hour', date.hour)
        set_user_data(chat_id, 'date', message.text)
        set_user_state(chat_id, 'booking_participants')

        bot.send_message(chat_id, get_message('bookingGuests'))
    except ValueError:
        bot.send_message(chat_id, get_message('wrongDateFormat'))


# 1.4.3. Гости
@bot.message_handler(func=lambda message: check_user_state(message.chat.id, 'booking_participants'))
def get_booking_participants(message):
    chat_id = message.chat.id

    try:
        participants = int(message.text)
        if participants < 1 or participants > 10:
            bot.send_message(chat_id, get_message('wrongGuestsValue'))
        else:
            set_user_data(chat_id, 'participants', participants)
            set_user_state(chat_id, 'booking_comment')

            bot.send_message(chat_id, get_message('bookingComment'))
    except ValueError:
        bot.send_message(chat_id, get_message('wrongGuestsFormat'))


# 1.4.4. Комментарий
@bot.message_handler(func=lambda message: check_user_state(message.chat.id, 'booking_comment'))
def get_booking_participants(message):
    chat_id = message.chat.id

    set_user_data(chat_id, 'comment', message.text)
    set_user_state(chat_id, 'booking_edit')

    bot.send_message(chat_id, get_message('bookingConfirmation'))
    confirm_message = bot.send_message(chat_id, get_booking_info(chat_id), reply_markup=confirmBookingMarkup)
    set_user_data(chat_id, 'confirm_message', confirm_message.message_id)


# 1.4.5. Редактирование брони
@bot.message_handler(func=lambda message: check_user_state(message.chat.id, 'booking_edit'))
def edit_form(message):
    chat_id = message.chat.id

    if not re.match("^[123]\. .+$", message.text):
        bot.send_message(chat_id, get_message('wrongFormat'))
        return

    if message.text[0] == '1':
        try:
            date = datetime.strptime(message.text[3:], '%d.%m.%Y %H:%M')
            set_user_data(chat_id, 'timeFrom', date.strftime('%Y-%m-%dT$H:00:00.000Z'))
            set_user_data(chat_id, 'date', message.text[3:])

            edit_booking_confirmation(chat_id)
        except ValueError:
            bot.send_message(chat_id, get_message('wrongDateFormat'))
    elif message.text[0] == '2':
        try:
            participants = int(message.text[3:])
            if participants < 1 or participants > 10:
                bot.send_message(chat_id, get_message('wrongGuestsValue'))
            else:
                set_user_data(chat_id, 'participants', participants)
                edit_booking_confirmation(chat_id)

        except ValueError:
            bot.send_message(chat_id, get_message('wrongGuestsFormat'))
    elif message.text[0] == '3':
        set_user_data(chat_id, 'comment', message.text[3:])
        edit_booking_confirmation(chat_id)


# 1.4.6. Мои брони
@bot.message_handler(func=lambda message: message.text == smileBookings)
def get_bookings(message):
    chat_id = message.chat.id
    res = get('/booking/by-user', {
        "userId": get_user_data(chat_id, 'userId')
    })
    bookings = [booking for booking in res['bookings'] if booking['status'] != 'CANCELLED']
    if not len(bookings):
        bot.send_message(chat_id, get_message('noBookings'))
    else:
        for booking in bookings:
            cancelBookingMarkup = types.InlineKeyboardMarkup()
            cancelBookingButton = types.InlineKeyboardButton('Отменить ❌', callback_data='cancelBooking-' + str(booking['id']))
            cancelBookingMarkup.row(cancelBookingButton)
            bot.send_message(chat_id, get_list_booking_info(booking), reply_markup=cancelBookingMarkup)


# 2. КоллБэк
@bot.callback_query_handler(func=lambda call: True)
def callback_confirm(call):
    chat_id = call.message.chat.id

    if call.data == 'start':
        set_user_state(chat_id, 'get_name')
        bot.send_message(chat_id, get_message('formName'), reply_markup=hide)
        hide_markup(chat_id)
    if call.data == 'confirmForm':
        res = post('/auth/login', {
            "name": get_user_data(chat_id, 'name'),
            "phone": get_user_data(chat_id, 'phone'),
            "chatId": chat_id,
            "expectedRole": "USER"
        })
        hide_markup(chat_id)
        set_user_data(chat_id, 'userId', res['userId'])
        bot.send_message(chat_id, 'На Ваш номер пришло СМС с кодом. Пожалуйста, отправьте код, чтобы подтвердить вход.',
                         reply_markup=hide)
        set_user_state(chat_id, 'get_code')
    if call.data == 'confirmBooking':
        res = get('/table/available', {
            'capacity': get_user_data(chat_id, 'participants'),
            'date': get_user_data(chat_id, 'timeFrom').split('T')[0]
        })

        hour = get_user_data(chat_id, 'hour')
        booking_table = None

        for table in res['tables']:
            st = [t[3] for t in table['availableStartTimes']]
            if hour in st:
                booking_table = table['name']
                break

        if booking_table:
            res = post('/booking/create', {
                'userId': get_user_data(chat_id, 'userId'),
                'name': '',
                'phone': '',
                "participants": get_user_data(chat_id, 'participants'),
                "tableName": booking_table,
                "timeFrom": get_user_data(chat_id, 'timeFrom'),
                "comment": get_user_data(chat_id, 'comment'),
                "platform": "TG"
            })
            hide_markup(chat_id)
            clear_user_data(chat_id)
            bot.send_message(chat_id, 'Столик забронирован!', reply_markup=userMarkup)
        else:
            bot.send_message(chat_id, 'К сожалению, свободных столов на это время нет..')
    if 'cancelBooking' in call.data:
        bookingId = int(call.data.split('-')[1])
        post('/booking/cancel', {
            "bookingId": bookingId
        })
        bot.send_message(chat_id, 'Бронь отменена!', reply_markup=userMarkup)
        bot.edit_message_text('ОТМЕНЕНА', chat_id=chat_id, message_id=call.message.id)
        hide_markup(chat_id, call.message.id)


# Редактирование сообщения-подтверждения
def edit_confirmation(chat_id):
    bot.send_message(chat_id, get_message('formCheck'))
    bot.edit_message_text(get_user_info(chat_id), chat_id=chat_id, message_id=get_user_data(chat_id, 'confirm_message'),
                          reply_markup=confirmFormMarkup)


def edit_booking_confirmation(chat_id):
    bot.send_message(chat_id, get_message('bookingCheck'))
    bot.edit_message_text(get_user_info(chat_id), chat_id=chat_id, message_id=get_user_data(chat_id, 'confirm_message'),
                          reply_markup=confirmBookingMarkup)


# Скрытие кнопки
def hide_markup(chat_id, message_id=None):
    if not message_id:
        message_id = get_user_data(chat_id, 'confirm_message')
    bot.edit_message_reply_markup(chat_id, message_id=message_id, reply_markup=hide_inline)
