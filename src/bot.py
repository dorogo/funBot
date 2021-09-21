import telebot
import sys
import re
import traceback
import pymorphy2
from utils.utils import Utils
from src.db.dbDriver import DbDriver


commands = ['/help - команды',
            '/getChatId - узнать id чата',
            '/addAllowedChat [chat_id] - добавть чат в разрешенные. личные чаты будут админами',
            '/removeAllowedChat [chat_id] - удалить чат из разрешенных',
            '/addMappingRow [key:value] - добавить в базу соответствие',
            '/deleteMappingRow phrase_id - удалить из базы соответствие',
            '/refreshCache - очистка кэша',
            '/turnOff - выкл бота']


class Bot:

    # user = None
    bot = None

    def init(self, token):
        try:
            self.bot = telebot.TeleBot(token)
            # self.user = self.bot.get_me()
        except telebot.apihelper.ApiTelegramException:
            print('Cant init bot.')
            sys.exit()
        # print(f'user = {self.user}')
        print('Connecting to db')
        db = DbDriver()

        @self.bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            chat_id = message.chat.id
            if not Utils.is_admin(chat_id):
                return
            result = "Commands:"
            for row in commands:
                result += "\n"+row
            self.bot.reply_to(message, result)

        @self.bot.message_handler(commands=['getChatId'])
        def send_chat_id(message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            if not Utils.is_admin(user_id):
                return
            self.bot.reply_to(message, chat_id)

        @self.bot.message_handler(commands=['addAllowedChat'])
        def add_allowed_chat(message):
            chat_id = message.chat.id
            if not Utils.is_admin(chat_id):
                return
            arr = message.text.split(' ')
            if len(arr) != 2:
                self.bot.reply_to(message, "Error. Command '/addAllowedChat chat_id'")
                return
            new_chat_id = arr[1]
            if db.add_chat_to_allowed(new_chat_id):
                self.bot.reply_to(message, f"Success. Chat {new_chat_id} added to allowed")
                Utils.refresh_chat_allowed()
            else:
                self.bot.reply_to(message, f"Error while adding chat {new_chat_id} to allowed")

        @self.bot.message_handler(commands=['removeAllowedChat'])
        def remove_allowed_chat(message):
            chat_id = message.chat.id
            if not Utils.is_admin(chat_id):
                return
            arr = message.text.split(' ')
            if len(arr) != 2:
                self.bot.reply_to(message, "Error. Command '/removeAllowedChat chat_id'")
                return
            chat_id_for_remove = arr[1]

            remove_result = db.remove_chat_to_allowed(chat_id_for_remove)
            result_msg = f"Chat {chat_id_for_remove} not found in allowed"
            if remove_result > 0:
                result_msg = f"Success. Chat {chat_id_for_remove} removed from allowed"
                Utils.refresh_chat_allowed()
            elif remove_result == -1:
                result_msg = f"Error while removing chat {chat_id_for_remove} from allowed"
            self.bot.reply_to(message, result_msg)

        @self.bot.message_handler(commands=['addMappingRow'])
        def add_row_to_mapping(message):
            chat_id = message.chat.id
            if not Utils.is_admin(chat_id):
                return False
            command = message.text
            index_separate = command.find(' ')
            if index_separate is None or index_separate < 1:
                self.bot.reply_to(message, f"Error. Command '/addMappingRow [key:value]'")
                return False
            command = command[index_separate+1:]
            arr = command.split(":")
            if len(arr) != 2:
                self.bot.reply_to(message, f"Error. Command '/addMappingRow [key:value]'")
                return False
            key = arr[0].lower()
            if key is None or len(key) < 1 or key.find(' ') != -1:
                self.bot.reply_to(message, f"Error. key '{key}' is not allowed")
                return False
            value = arr[1]
            if value is None or len(value) < 1:
                self.bot.reply_to(message, f"Error. value '{value}' is not allowed")
                return False
            if db.add_row_to_mapping(key, value):
                self.bot.reply_to(message, f"Success. Row '{key}':'{value}' added to mapping")
            else:
                self.bot.reply_to(message, f"Error while adding row '{key}':'{value}' added to mapping")
                return False
            return True

        @self.bot.message_handler(commands=['deleteMappingRow'])
        def delete_row_from_mapping(message):
            chat_id = message.chat.id
            if not Utils.is_admin(chat_id):
                return
            arr = message.text.split(' ')
            if len(arr) != 2:
                self.bot.reply_to(message, "Error. Command '/deleteMappingRow phrase_id'")
                return
            phrase_id_for_remove = arr[1]
            remove_result = db.remove_row_from_mapping(phrase_id_for_remove)
            result_msg = f"Phrase_id '{phrase_id_for_remove}' not found in mapping"
            if remove_result > 0:
                result_msg = f"Success. Phrase_id '{phrase_id_for_remove}' removed from mapping"
            elif remove_result == -1:
                result_msg = f"Error while removing phrase_id '{phrase_id_for_remove}' from mapping"
            self.bot.reply_to(message, result_msg)

        @self.bot.message_handler(commands=['refreshCache'])
        def refresh_cache(message):
            chat_id = message.chat.id
            if not Utils.is_admin(chat_id):
                print(f" Chat id='{chat_id}' is not admin")
                return
            if Utils.refresh_chat_allowed():
                print("Refreshed allowed chats")
                self.bot.reply_to(message, "Refreshed allowed chats")

        @self.bot.message_handler(commands=['turnOff'])
        def turn_off(message):
            chat_id = message.chat.id
            if not Utils.is_admin(chat_id):
                print(f" Chat id='{chat_id}' is not admin")
                return
            self.bot.stop_polling()
            sys.exit()

        morph = pymorphy2.MorphAnalyzer()

        @self.bot.message_handler()
        def echo_all(message):
            chat_id = message.chat.id
            # self.bot.send_sticker(chat_id, 'CAADAgADOQADfyesDlKEqOOd72VKAg', message.message_id)
            if not Utils.is_chat_allowed(chat_id):
                print(f" Chat id='{chat_id}' is not allowed")
                return
            print(f'message.text = >{message.text}< chat_id = {chat_id}')
            source_message = re.sub('[^а-яА-Я ]+', '', message.text)
            print(source_message)
            source_message = re.sub('[^а-яА-Яa-zA-z ]+', '', message.text)
            arr_words = source_message.split(' ')
            result = None
            for w in arr_words:
                if len(w) == 0 or w == ' ':
                    continue
                print(f"processing '{w}'")
                result = self.process_word(db, w, morph)
                if result is not None:
                    break
            if result is None or len(result) == 0:
                print('Empty result')
                return
            print(f'res = >{result}< ')
            # self.bot.send_message(chat_id, result)
            self.bot.reply_to(message, result)

        @self.bot.message_handler(content_types=['sticker'])
        def echo_sticker(message):
            chat_id = message.chat.id
            if not Utils.is_admin(chat_id):
                print(f" Chat id='{chat_id}' is not admin")
                return
            sticker_id = message.sticker.file_id
            self.bot.reply_to(message, sticker_id)


    def start(self):
        self.bot.polling()

    def process_word(self, db, word, morph):
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

    pass
