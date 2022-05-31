# import pymysql
# 使用MySQL原生语句
from django.db import connection


class Exsql():
    '''
    配合django 内置的数据库操作函数使用
    '''

    def __init__(self):
        pass

    def get_one(self, sql, *args) -> tuple:
        res = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, args)  # 需要先执行
                res = cursor.fetchone()
        except Exception as e:
            raise e
        return res

    def get_one_dict(self, sql, *args) -> list:
        res = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, args)  # 需要先执行
                desc = cursor.description
                res = [
                    dict(zip([col[0] for col in desc], cursor.fetchone()))]
        except Exception as e:
            raise e
        return res

    def get_all(self, sql, *args) -> tuple:
        res = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, args)  # 需要先执行
                res = cursor.fetchall()
        except Exception as e:
            raise e
        return res

    def get_all_dict(self, sql, *args) -> list:
        res = []
        """抛出异常，交给视图处理"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, args)  # 需要先执行
                desc = cursor.description
                res = [
                    dict(zip([col[0] for col in desc], row))
                    for row in cursor.fetchall()
                ]
        except Exception as e:
            raise e
        return res

        """
        捕捉异常
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, args)  # 需要先执行
                desc = cursor.description
                res = [
                    dict(zip([col[0] for col in desc], row))
                    for row in cursor.fetchall()
                ]

        except Exception as e:
            res = {'code': 1, 'error': e}
        return res
        """

    def insert(self, sql, *args):
        return self.__edit(sql, *args)

    def update(self, sql, *args):
        return self.__edit(sql, *args)

    def delete(self, sql, *args):
        return self.__edit(sql, *args)

    #返回操作的数据行数
    def __edit(self, sql, *args) -> int:
        count = 0
        cursor = connection.cursor()
        try:
            count = cursor.execute(sql, args)
        except Exception as e:
            # res = {'code': 1, 'error': e}
            cursor.rollback()
            raise e
        finally:
            cursor.close()
        return count
