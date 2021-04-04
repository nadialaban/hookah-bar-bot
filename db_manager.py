import sqlalchemy
from sqlalchemy import create_engine
from config import *

# 1. Подключение к бд.
db_string = "postgres://{}:{}@{}:{}/{}".format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
db = create_engine(db_string)


# 2. Описание моделей
# 2.1. Сообщение от бота
class BotMessage(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Text, primary_key=True)
    message = db.Column(db.Text)
    description = db.Column(db.Text)


# 2.1. Пользователь
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    status = db.Column(db.Text)
    phone = db.Column(db.Text)
    birthday = db.Column(db.Date)
    confirmed = db.Column(db.Boolean)
    confirm_msg = db.Column(db.Integer)
    action = db.Column(db.Text)


def get_message(msg_id):
    msg = BotMessage.query.filter_by(id=msg_id).first()
    if msg is not None:
        return msg.message
    return 'unexpected type'