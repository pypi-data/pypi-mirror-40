import pickle
import os
import sys

YTINY_PATH = os.path.dirname(sys.argv[0])+os.sep+'ytiny'
if os.path.exists(YTINY_PATH):
    if os.path.isfile(YTINY_PATH):
        raise FileNotFoundError(YTINY_PATH+" is file, but ytiny want a dir ")
else:
    os.mkdir(YTINY_PATH)

USER_INFO_FILE_NAME = YTINY_PATH+os.sep+'userinfo'


def load_user():
    f = open(USER_INFO_FILE_NAME, 'rb')
    return pickle.load(f)


def dump_user_mutual():
    if user_info_exists():
        print('输入r:\t\t重新设定账户信息')
        print('其他输入:\t使用上次账户信息')
        first_input = input()
        if first_input == 'r':
            dump_user()
            print('使用重新设定的账户信息登录')

    else:
        dump_user()
        print('使用上次的账户信息登录')


def dump_user(username=None, password=None):
    if username is None and password is None:
        username, password = __input_user_info()

    f = open(USER_INFO_FILE_NAME, 'wb')
    pickle.dump((username, password), f)
    f.close()


def user_info_exists():
    return os.path.exists(USER_INFO_FILE_NAME)


def __input_user_info():
    return input('username: '), input('password: ')

