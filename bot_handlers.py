from bot import *


# 1. Обработчики команд пользователя
# 1.1. Приветствие
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    bot.send_message(user_id, get_message('greeting'), reply_markup=hide)
    bot.send_message(user_id, get_message('startFormText'), reply_markup=startFormMarkup)
