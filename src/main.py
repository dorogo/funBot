import traceback
import telebot
import sys
from db.dbDriver import DbDriver
import pymorphy2
import re
from utils.utils import Utils
from telebot import types


if __name__ == '__main__':

    def process_word(word):
        # попробуем найти исходное слово в бд
        result = db.getById(word)
        if result is not None:
            return result

        # не нашли, пробуем получить начальную форму слова и искать его
        try:
            morphed_words = morph.parse(word)
        except Exception:
            traceback.print_exc()
            return None
        # print(f"morphed_words: {morphed_words}")
        for q in morphed_words:
            result = db.getById(q.normal_form)
            if result is not None:
                break
        return result


    # execution
    print("it's started!")

    morph = pymorphy2.MorphAnalyzer()

    # получаем токен из cfg файла
    with open('../conf/my.cfg', 'r') as cfg:
        token = cfg.read()
        if token is None:
            print("Cant find bot token")
            sys.exit()

    print(f'token = {token}')
    try:
        bot = telebot.TeleBot(token)
        user = bot.get_me()
    except telebot.apihelper.ApiTelegramException:
        print('Cant init bot.')
        sys.exit()

    print(f'user = {user}')

    print('Connecting to db')
    db = DbDriver()


    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        print(message.message_id)
        bot.reply_to(message, "Trun' pososi")

    @bot.message_handler(commands=['refreshCache','refreshcache'])
    def send_welcome(message):
        chat_id = message.chat.id
        if not Utils.is_admin(chat_id):
            print(f" Chat id='{chat_id}' is not admin")
            return
        if Utils.refresh_chat_allowed():
            print("Refreshed allowed chats")
            bot.reply_to(message, "Refreshed allowed chats")


    @bot.message_handler()
    def echo_all(message):
        chat_id = message.chat.id
        if not Utils.is_chat_allowed(chat_id):
            print(f" Chat id='{chat_id}' is not allowed")
            return
        print(f'message.text = >{message.text}< chat_id = {chat_id}')
        source_message = re.sub('[^а-яА-Я ]+', '', message.text)
        print(source_message)
        arr_words = source_message.split(' ')
        result = None
        for w in arr_words:
            if len(w) == 0 or w == ' ':
                continue
            print(f"processing '{w}'")
            result = process_word(w)
            if result is not None:
                break
        if result is None or len(result) == 0:
            print('Empty result')
            return
        print(f'res = >{result}< ')
        # bot.send_message(chat_id, result)
        bot.reply_to(message, result)


    bot.polling()
