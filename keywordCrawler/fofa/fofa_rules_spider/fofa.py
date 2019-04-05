# -*- coding: utf-8 -*-
# @File  : fofa.py.py
# @Author: TT
# @Email : tt.jiaqi@gmail.com
# @Date  : 2019/4/1
# @Desc  : 
import requests

from scrapy.selector import Selector
import sys
import json
import pymysql


test_data = '  <span style="margin-right: 7px;" data-rule_name="天融信-网络审计系统">\n    <a href="/library", class="text-muted"> 天融信-网络审计系统 &nbsp;&nbsp; </a>\n  </span>\n  <span style="margin-right: 7px;" data-rule_name="明御综合日志审计">\n    <a href="/library", class="text-muted"> 明御综合日志审计 &nbsp;&nbsp; </a>\n  </span>\n  <span style="margin-right: 7px;" data-rule_name="思福迪-LOGBASE日志管理综合审计系统">\n    <a href="/library", class="text-muted"> 思福迪-LOGBASE日志管理综合审计系统 &nbsp;&nbsp; </a>\n  </span>\n  <span style="margin-right: 7px;" data-rule_name="江南科友-HAC">\n    <a href="/library", class="text-muted"> 江南科友-HAC &nbsp;&nbsp; </a>\n  </span>\n  <span style="margin-right: 7px;" data-rule_name="OMAudit">\n    <a href="/library", class="text-muted"> OMAudit &nbsp;&nbsp; </a>\n  </span>\n  <span style="margin-right: 7px;" data-rule_name="H3C-SecPath-运维审计系统">\n    <a href="/library", class="text-muted"> H3C-SecPath-运维审计系统 &nbsp;&nbsp; </a>\n  </span>\n  <span style="margin-right: 7px;" data-rule_name="启明星辰-天玥网络安全审计">\n    <a href="/library", class="text-muted"> 启明星辰-天玥网络安全审计 &nbsp;&nbsp; </a>\n  </span>\n  <span style="margin-right: 7px;" data-rule_name="网神-SecFox">\n    <a href="/library", class="text-muted"> 网神-SecFox &nbsp;&nbsp; </a>\n  </span>\n  <span style="margin-right: 7px;" data-rule_name="网御-网络审计系统">\n    <a href="/library", class="text-muted"> 网御-网络审计系统 &nbsp;&nbsp; </a>\n  </span>\n  <span style="margin-right: 7px;" data-rule_name="中科新业网络哨兵">\n    <a href="/library", class="text-muted"> 中科新业网络哨兵 &nbsp;&nbsp; </a>\n  </span>\n  <span style="margin-right: 7px;" data-rule_name="HAC运维安全审计系统">\n    <a href="/library", class="text-muted"> HAC运维安全审计系统 &nbsp;&nbsp; </a>\n  </span>\n'


def spider_libary(url):
    type_dict = {}
    headers = {
        'Host' : 'fofa.so',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)

        #print(response)
    except Exception as e:
        print(e)
        sys.exit(0)

    a_sel = Selector(text=response.text)
    data_list = a_sel.css('.container .mar_t30 .col-xs-12')
    for data in data_list:
        type_name = data.css('label::text').extract()[0]
        type_id = data.css('div::attr("data-category_id")').extract()[0]
        type_dict[type_name] = type_id

    return type_dict


def get_data(type_dict):
    data_dict = {}
    headers = {
        'Host': 'fofa.so',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    url = "https://fofa.so/ajax/get_category_rules?category_id={}"
    for key,value in type_dict.items():
        try:
            response = requests.get(url.format(value))
        except Exception as e:
            print(e)
        json_data = json.loads(response.text)
        r = Selector(text=json_data['html'])
        rule_list = r.css("span::attr('data-rule_name')").extract()
        data_dict[key] = rule_list
        print(data_dict[key])

    return data_dict


def connect_mysql(date_dict):
    try:
        conn = pymysql.connect(host='127.0.0.1',port=3306, user='root', passwd='root', db='rules')
    except Exception as e:
        print(e)
        sys.exit(0)
    for key,value in date_dict.items():
        cursor = conn.cursor()
        cursor.executemany("insert into rules(rule_name,rule_content) values (%s,%s)", [(key, str(value))])
        conn.commit()
        cursor.close()


if __name__ == "__main__":
    start_url = "https://fofa.so/library"
    type_dict = spider_libary(url=start_url)
    data_dict = get_data(type_dict)
    print(data_dict)

    connect_mysql(data_dict)