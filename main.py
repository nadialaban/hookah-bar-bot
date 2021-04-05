from bot_handlers import *
import time
from threading import Thread


def start():
    while True:
        try:
            bot.polling(none_stop=True, timeout=123)
        except Exception as e:
            time.sleep(5)


if __name__ == '__main__':
    # thread_bday = Thread(target=birthday_congrats)
    # thread_bday.start()
    main_thread = Thread(target=start)
    main_thread.start()

