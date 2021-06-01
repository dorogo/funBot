import traceback
import telebot
import sys
from db.dbDriver import DbDriver
import pymorphy2
import re
from utils.utils import Utils
from telebot import types


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


commands = ['/help - команды',
            '/getChatId - узнать id чата',
            '/addAllowedChat [chat_id] - добавть чат в разрешенные. личные чаты будут админами',
            '/removeAllowedChat [chat_id] - удалить чат из разрешенных',
            '/addMappingRow [key:value]',
            '/refreshCache - очистка кэша']


if __name__ == '__main__':
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
        chat_id = message.chat.id
        if not Utils.is_admin(chat_id):
            return
        result = "Commands:"
        for row in commands:
            result += "\n"+row
        bot.reply_to(message, result)

    @bot.message_handler(commands=['getChatId'])
    def send_chat_id(message):
        chat_id = message.chat.id
        if chat_id > 0:
            bot.reply_to(message, chat_id)

    @bot.message_handler(commands=['addAllowedChat'])
    def add_allowed_chat(message):
        chat_id = message.chat.id
        if not Utils.is_admin(chat_id):
            return
        arr = message.text.split(' ')
        if len(arr) != 2:
            bot.reply_to(message, "Error. Command '/addAllowedChat chat_id'")
            return
        new_chat_id = arr[1]
        if db.add_chat_to_allowed(new_chat_id):
            bot.reply_to(message, f"Success. Chat {new_chat_id} added to allowed")
            Utils.refresh_chat_allowed()
        else:
            bot.reply_to(message, f"Error while adding chat {new_chat_id} to allowed")


    @bot.message_handler(commands=['removeAllowedChat'])
    def remove_allowed_chat(message):
        chat_id = message.chat.id
        if not Utils.is_admin(chat_id):
            return
        arr = message.text.split(' ')
        if len(arr) != 2:
            bot.reply_to(message, "Error. Command '/removeAllowedChat chat_id'")
            return
        chat_id_for_remove = arr[1]

        remove_result = db.remove_chat_to_allowed(chat_id_for_remove)
        result_msg = f"Chat {chat_id_for_remove} not found in allowed"
        if remove_result > 0:
            result_msg = f"Success. Chat {chat_id_for_remove} removed from allowed"
            Utils.refresh_chat_allowed()
        elif remove_result == -1:
            result_msg = f"Error while removing chat {chat_id_for_remove} from allowed"
        bot.reply_to(message, result_msg)

    @bot.message_handler(commands=['addMappingRow'])
    def add_row_to_mapping(message):
        chat_id = message.chat.id
        if not Utils.is_admin(chat_id):
            return False
        command = message.text
        index_separate = command.find(' ')
        if index_separate is None or index_separate < 1:
            bot.reply_to(message, f"Error. Command '/addMappingRow [key:value]'")
            return False
        command = command[index_separate+1:]
        arr = command.split(":")
        if len(arr) != 2:
            bot.reply_to(message, f"Error. Command '/addMappingRow [key:value]'")
            return False
        key = arr[0].lower()
        if key is None or len(key) < 1 or key.find(' ') != -1:
            bot.reply_to(message, f"Error. key '{key}' is not allowed")
            return False
        value = arr[1]
        if value is None or len(value) < 1:
            bot.reply_to(message, f"Error. value '{value}' is not allowed")
            return False
        if db.add_row_to_mapping(key, value):
            bot.reply_to(message, f"Success. Row '{key}':'{value}' added to mapping")
        else:
            bot.reply_to(message, f"Error while adding row '{key}':'{value}' added to mapping")
            return False
        return True





    @bot.message_handler(commands=['refreshCache'])
    def refresh_cache(message):
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
        # bot.send_sticker(chat_id, 'CAADAgADOQADfyesDlKEqOOd72VKAg', message.message_id)
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
