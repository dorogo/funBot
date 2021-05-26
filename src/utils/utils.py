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
