# -*- coding: utf-8 -*-
# @File  : zoomcat_keyword.py
# @Author: TT
# @Email : tt.jiaqi@gmail.com
# @Date  : 2019/4/10
# @Desc  : 
import pymysql
import requests
import sys

from scrapy.selector import Selector

def gethtml(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)

        # print(response)
    except Exception as e:
        print(e)
        sys.exit(0)

    return response.text


def get_keyword(response):
    selector = Selector(text=response)
    a_s = selector.css("body div a::attr(href)").extract()
    result_list = []
    for a in a_s:
        result_list.append(a.split('/')[-1])

    return result_list


def insert_mysql(result_list):
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='rules')
    except Exception as e:
        print(e)
        sys.exit(0)
    for result in result_list:
        cursor = conn.cursor()
        cursor.executemany("insert into zoomcat_keyword(keyword) values (%s)", [(result)])
        conn.commit()
        cursor.close()
        print("insert into zoomcat_keyword(keyword) values ({})".format(result))


if __name__ == "__main__":
    start_url = "https://zoomcat.fht.im/"
    response = gethtml(start_url)
    result_list = get_keyword(response)
    insert_mysql(result_list)
