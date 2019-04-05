# -*- coding: utf-8 -*-
# @File  : zoomeye.py
# @Author: TT
# @Email : tt.jiaqi@gmail.com
# @Date  : 2019/4/4
# @Desc  :

import pymysql
import sys


text = """
    此处为https://www.zoomeye.org/collection/component返回的数据
"""


def connect_mysql(conn,rule,types):
    cursor = conn.cursor()
    cursor.executemany("insert into rules(rule_name,rule_type) values (%s,%s)", [(rule, str(types))])
    conn.commit()
    cursor.close()


if __name__ == "__main__":
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='rules')
    except Exception as e:
        print(e)
        sys.exit(0)

    for a in text:
        connect_mysql(conn,a['name'],a['type'])
        print(a['name'],a['type'])