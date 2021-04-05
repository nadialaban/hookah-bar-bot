from bot import *
import re
from datetime import datetime


# 1. Обработчики команд пользователя
# 1.1. Приветствие
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    bot.send_message(user_id, get_message('greeting'), reply_markup=hide)
    bot.send_message(user_id, get_message('startForm'), reply_markup=startFormMarkup)


# 1.2. Анкета
# 1.2.1. Имя
@bot.message_handler(func=lambda message: get_user(message.chat.id).action == 'get_name')
def get_name(message):
    user_id = message.chat.id
    user = get_user(user_id)

    if re.match("^[А-Яа-я ёЁ-]+$", message.text):
        user.set_name(message.text)
        user.set_action('get_birthday')
        bot.send_message(user_id, 'Привет, {}!\n{}'.format(message.text, get_message('formBDay')), reply_markup=hide)
    else:
        bot.send_message(user_id, get_message('wrongNameFormat'))


# 1.2.2. ДР
@bot.message_handler(func=lambda message: get_user(message.chat.id).action == 'get_birthday')
def get_birthday(message):
    user_id = message.chat.id
    user = get_user(user_id)

    try:
        date = datetime.strptime(message.text, '%d.%m')
        user.set_birthday(date)
        user.set_action('get_phone')
        bot.send_message(user_id, get_message('formPhone'))
    except ValueError:
        bot.send_message(user_id, get_message('wrongDateFormat'))


# 1.2.3. Номер телефона
@bot.message_handler(func=lambda message: get_user(message.chat.id).action == 'get_phone')
def get_phone(message):
    user_id = message.chat.id
    user = get_user(user_id)

    if re.match("^(\+7|8)(-|–|—|\s)?\(?(9\d{2})\)?(-|–|—|\s)?(\d{3})(-|–|—|\s)?(\d{2})(-|–|—|\s)?(\d{2})$", message.text):
        user.set_phone(message.text)

        user.set_action('edit')
        bot.send_message(user_id, get_message('formConfirmation'))
        confirm_message = bot.send_message(user_id, user.get_info(), reply_markup=confirmFormMarkup)
        user.set_msg(confirm_message.message_id)
    else:
        bot.send_message(user_id, get_message('wrongPhoneFormat'))


# 1.2.4. Редактирование формы
@bot.message_handler(func=lambda message: get_user(message.chat.id).action == 'edit')
def edit_form(message):
    user_id = message.chat.id
    user = get_user(user_id)

    if not re.match("^[1-3]\. .+$", message.text):
        bot.send_message(user_id, get_message('wrongFormat'))
        return

    if message.text[0] == '1':
        if re.match("^[А-Яа-я ёЁ]*$", message.text[3:]):
            user.set_name(message.text[3:])
            edit_confirmation(user)
        else:
            bot.send_message(user_id, get_message('wrongNameFormat'))

    elif message.text[0] == '2':
        try:
            date = datetime.strptime(message.text, '%d.%m')
            user.set_birthday(date)
            bot.send_message(user_id, get_message('formPhone'))
        except ValueError:
            bot.send_message(user_id, get_message('wrongDateFormat'))

    elif message.text[0] == '3':
        if re.match("^(\+7|8)(-|–|—|\s)?\(?(9\d{2})\)?(-|–|—|\s)?(\d{3})(-|–|—|\s)?(\d{2})(-|–|—|\s)?(\d{2})$", message.text):
            user.set_phone(message.text[3:])
            edit_confirmation(user)
        else:
            bot.send_message(user_id, get_message('wrongPhoneFormat'))


# 5.5. КоллБэк
@bot.callback_query_handler(func=lambda call: True)
def callback_confirm(call):
    user_id = call.message.chat.id
    user = create_user(user_id)

    if call.data == 'start':
        if user.name is not None:
            bot.send_message(user_id, get_message('userExists') + "{}?".format(user.name), reply_markup=secondConfirmFormMarkup)
        else:
            bot.send_message(user_id, get_message('formName'), reply_markup=hide)

    elif call.data == 'me':
        bot.send_message(user_id, get_message('formConfirmation'), reply_markup=hide)
        confirm_message = bot.send_message(user_id, user.get_info(), reply_markup=confirmFormMarkup)
        user.set_msg(confirm_message.message_id)
        user.set_action('edit')
    elif call.data == 'notMe':
        user.reset()
        bot.send_message(user_id, get_message('newForm'), reply_markup=hide)
        bot.send_message(user_id, get_message('formName'))


# Редактирование сообщения-подтвержения
def edit_confirmation(user):
    bot.send_message(user.id, get_message('formCheck'))
    bot.edit_message_text(user.get_info(), chat_id=user.id, message_id=user.confirm_msg, reply_markup=confirmFormEditMarkup)
