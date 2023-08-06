import pickle
import os
import sys
import hashlib

v = os.path.dirname(sys.argv[0])
LLUSER_PATH = v + os.sep + 'lluser'
if os.path.exists(LLUSER_PATH):
    if os.path.isfile(LLUSER_PATH):
        raise FileNotFoundError(LLUSER_PATH + " is file, but lluser want a dir ")
else:
    os.mkdir(LLUSER_PATH)

USER_INFO_FILE_NAME = LLUSER_PATH + os.sep + 'userinfo-' + hashlib.md5(LLUSER_PATH.encode('utf-8')).hexdigest()


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
            print('使用上次的账户信息登录')
    else:
        print('首次设置的账户信息登录')
        dump_user()


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

