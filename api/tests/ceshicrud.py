import sys
import os
import django

# # 这两行很重要，用来寻找项目根目录，os.path.dirname要写多少个根据要运行的python文件到根目录的层数决定
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(BASE_DIR)
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutorial.settings')
django.setup()
from utils.crud import Exsql
from api import models


def md5(username):
    import hashlib
    import time
    ctime = str(time.time())
    m = hashlib.md5(bytes(username, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


def crud_getdict():
    c = Exsql()
    pwd = '123'
    user = 'liuzhu'
    userid = c.get_one('''select id from api_userinfo where password = %s AND  username = %s''', pwd, user)
    count = c.get_one('''select count(1) from api_usertoken where user_id = %s''', userid[0])
    token = md5(user)

    print (userid, count, count[0], token)
    if count[0] == 0:
        with transaction.atomic():
            c.insert('''insert into api_usertoken(token,user_id) values (%s,%s)''', token, userid[0])
    else:
        with transaction.atomic():
            c.update('''update api_usertoken set token=%s where user_id=%s''', token, userid[0])

def fun1():
    ret = models.Role.objects.all()
    ret = ret.values('id', 'role')
    # ret = list(ret)
    print(type(ret), ret[0]['id'])


if __name__ == '__main__':
    # crud_getdict()
    fun1()