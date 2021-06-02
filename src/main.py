from bot import Bot
import sys

if __name__ == '__main__':
    print("it's started!")
    # получаем токен из cfg файла
    with open('../conf/my.cfg', 'r') as cfg:
        token = cfg.read()
        if token is None:
            print("Cant find bot token")
            sys.exit()
    print(f'token = {token}')
    bot = Bot()
    bot.init(token)
    bot.start()
    pass
