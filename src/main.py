from bot import Bot
import sys
import os


# Disable
def block_print():
    sys.stdout = open(os.devnull, 'w')


if __name__ == '__main__':
    print("it's started!")
    if 'blockPrint' in sys.argv:
        block_print()
    # получаем токен из cfg файла
    with open('../conf/my.cfg', 'r') as cfg:
        token = cfg.read()
        if token is None:
            print("Cant find bot token")
            sys.exit()
    bot = Bot()
    bot.init(token)
    bot.start()
    pass
