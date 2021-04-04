import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import *

# 1. Подключение к бд.
db_string = "postgres://{}:{}@{}:{}/{}".format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
db = create_engine(db_string)
base = declarative_base()
Session = sessionmaker(db)
session = Session()


# 2. Описание моделей
# 2.1. Сообщение от бота
class BotMessage(base):
    __tablename__ = 'messages'

    id = Column(sqlalchemy.Text, primary_key=True)
    message = Column(sqlalchemy.Text)
    description = Column(sqlalchemy.Text)


# 2.1. Пользователь
class User(base):
    __tablename__ = 'users'

    id = Column(sqlalchemy.Integer, primary_key=True)
    name = Column(sqlalchemy.Text)
    status = Column(sqlalchemy.Text)
    phone = Column(sqlalchemy.Text)
    birthday = Column(sqlalchemy.Date)
    confirmed = Column(sqlalchemy.Boolean)
    confirm_msg = Column(sqlalchemy.Integer)
    action = Column(sqlalchemy.Text)


def get_message(msg_id):
    msg = db.execute("SELECT * FROM messages WHERE id=" + str(msg_id))
    if msg is not None:
        return msg.message
    return 'unexpected type'
