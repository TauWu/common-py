# -*- coding: utf-8 -*-

import pymysql
from pymysql.err import IntegrityError

class DBController(object):

    def __init__(self):
        self.init_mysql()

    def init_mysql(self):
        cfg = dict(
            host="127.0.0.1",
            port=3306,
            user="root",
            passwd="123123abc",
            db="data"
        )

        print(cfg["host"], cfg["port"], cfg["user"], cfg["passwd"], cfg["db"], "utf8")

        try:
            self._conn = pymysql.connect(
                host="127.0.0.1", port=3306, user="root",
                passwd="123123abc", db="data", charset="utf8"
            )
        except Exception as e:
            print("数据库连接创建失败！[{}] {}".format(cfg, e))

        self.cur = self._conn.cursor()
        self.IntegrityError = IntegrityError

    def execute(self, SQL):
        self.cur.execute(SQL)
        self._conn.commit()

    def close(self):
        self.cur.close()
        self._conn.close()