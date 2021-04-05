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

    def set_name(self, name):
        self.name = name
        session.add(self)
        session.commit()

    def set_phone(self, phone):
        self.phone = phone
        session.add(self)
        session.commit()

    def set_birthday(self, birthday):
        self.birthday = birthday
        session.add(self)
        session.commit()

    def set_action(self, action):
        self.action = action
        session.add(self)
        session.commit()

    def set_msg(self, msg):
        self.confirm_msg = msg
        session.add(self)
        session.commit()

    def set_confirmed(self, confirmed):
        self.confirmed = confirmed
        session.add(self)
        session.commit()

    def reset(self):
        self.name = None
        self.birthday = None
        self.phone = None
        self.confirm_msg = None
        self.confirmed = False
        self.action = 'get_name'
        session.add(self)
        session.commit()

    def get_info(self):
        return '1. Имя: {}\n'.format(self.name) + \
               '2. День рождения: {}\n'.format(self.birthday.strftime('%d.%m')) + \
               '3. Номер: {}'.format(self.phone)


# 3. Методы для работы с бд
# 3.1. Получение сообщения по айди
def get_message(msg_id):
    msg = session.query(BotMessage).filter_by(id=msg_id).first()
    if msg is not None:
        return msg.message
    return 'unexpected type'


# 3.2. Получение пользователя по айди
def get_user(user_id):
    return session.query(User).filter_by(id=user_id).first()


# 3.3. Создание пользователя
def create_user(user_id):
    user = get_user(user_id)

    if user is not None:
        user.confirmed = False
        user.action = ''
        session.commit()
        return user
    user = User(id=user_id, confirmed=False,
                action='get_name', status='guest')

    session.add(user)
    session.commit()
    return user



