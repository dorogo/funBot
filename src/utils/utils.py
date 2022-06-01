from src.db.dbDriver import DbDriver

allowed_chats = None


class Utils:

    # если chat_id > 0 - чат личный, если отрицательный - чат групповой
    @staticmethod
    def is_admin(chat_id):
        return chat_id > 0 and Utils.is_chat_allowed(chat_id)

    @staticmethod
    def is_chat_allowed(chat_id):
        if chat_id is None:
            return False
        global allowed_chats
        if allowed_chats is None:
            db = DbDriver()
            allowed_chats = db.getAllowedChats()
            print(allowed_chats)
        return chat_id in allowed_chats

    @staticmethod
    def refresh_chat_allowed():
        global allowed_chats
        allowed_chats = None
        print("Refreshed cache allowed chats")
        return True

    @staticmethod
    def add_row_to_mapping(message):
        chat_id = message.chat.id
        print(f'chat_id {chat_id}')
        if not Utils.is_admin(chat_id):
            return False
        command = message.text
        print(f'command {command}')
        index_separate = command.find(' ')
        if index_separate is None or index_separate < 1:
            return False
        command = command[index_separate + 1:]
        arr = command.split(":")
        if len(arr) != 2:
            return False
        key = arr[0].lower()
        if key is None or len(key) < 1 or key.find(' ') != -1:
            return False
        value = arr[1]
        if value is None or len(value) < 1:
            return False
        # db = DbDriver()
        # if db.add_row_to_mapping(key, value):
        #     # bot.reply_to(message, f"Success. Row '{key}':'{value}' added to mapping")
        #     print("asd")
        # else:
        #     # bot.reply_to(message, f"Error while adding row '{key}':'{value}' added to mapping")
        #     return False
        return True
