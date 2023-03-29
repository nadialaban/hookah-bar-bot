from config import *
import json
import requests


def read_json(file_name):
    f = open(file_name, 'r')
    json_data = f.read()
    f.close()
    return json.loads(json_data)


def save_users():
    global users
    json_data = json.dumps(users, indent=6, ensure_ascii=False)
    f = open("users.json", 'w')
    f.write(json_data)
    f.close()


def get(route, params=None):
    res = requests.get(api_host + route, params)
    return res.json()


def post(route, data):
    res = requests.post(api_host + route, json=data)
    return res.json()


def add_user(chat_id):
    global users
    chat_id = str(chat_id)
    users[chat_id] = {
        'state': 'started',
        'data': {
            'chatId': chat_id,
            'name': '',
            'phone': '',
            'userId': None,
            'confirm_message': None
        }
    }
    save_users()


def set_user_state(chat_id, state):
    global users
    chat_id = str(chat_id)
    if chat_id in users:
        users[chat_id]['state'] = state
    save_users()


def check_user_state(chat_id, state):
    global users
    chat_id = str(chat_id)
    return chat_id in users and users[chat_id]['state'] == state


def set_user_data(chat_id, field, data):
    global users
    chat_id = str(chat_id)
    if chat_id in users:
        users[chat_id]['data'][field] = data
    save_users()


def clear_user_data(chat_id):
    global users
    chat_id = str(chat_id)
    if chat_id in users:
        users[chat_id]['state'] = None
        try:
            users[chat_id]['data'].pop('name')
            users[chat_id]['data'].pop('phone')
            users[chat_id]['data'].pop('chatId')
        except:
            pass
        try:
            users[chat_id]['data'].pop('date')
            users[chat_id]['data'].pop('timeFrom')
            users[chat_id]['data'].pop('participants')
            users[chat_id]['data'].pop('comment')
        except:
            pass
        users[chat_id]['data']['confirm_message'] = None
    save_users()


def get_user_data(chat_id, field):
    global users
    chat_id = str(chat_id)
    if chat_id in users:
        return users[chat_id]['data'][field]
    return None


def get_user_info(chat_id):
    global users
    chat_id = str(chat_id)
    if chat_id in users:
        return '1. Имя: ' + users[chat_id]['data']['name'] + \
               '\n2.Номер телефона:' + users[chat_id]['data']['phone']


def get_booking_info(chat_id):
    global users
    chat_id = str(chat_id)
    if chat_id in users:
        return '1. Дата и время: ' + users[chat_id]['data']['date'] + \
               '\n2. Количество гостей: ' + str(users[chat_id]['data']['participants']) + \
               '\n3. Комментарий: ' + users[chat_id]['data']['comment']


def get_list_booking_info(booking):
    date = booking["startTime"]
    return 'Дата и время: {:0>2d}.{:0>2d} в {:0>2d}:00'.format(date[2], date[1], date[3]) + \
        '\nКоличество гостей: ' + str(booking['participants']) + \
           '\nКомментарий: ' + booking['comment']

def get_link(link):
    global messages
    return messages['links'][link]


def get_message(message):
    global messages
    return messages['messages'][message]


messages = read_json('messages.json')
users = read_json('users.json')
