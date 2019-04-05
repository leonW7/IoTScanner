# -*- coding: utf-8 -*-
# @File     : main.py
# @Author   : TT
# @Email    : tt.jiaqi@gmail.com
# @Date     : 19-2-12 上午10:51
# @Desc     : Main Running Documents

# ftp://ftp2.dlink.com/
from lib.spider import Spider, Dlink_info
from lib.config import SAVE_PATH
from lib.general import TraverFile, RUNS
from lib.mail import Email

import datetime
import time


def spider_run():
    t = TraverFile(SAVE_PATH)
    t.find_already_firmware()
    file_dict = t.get_filepath()

    print(file_dict)
    if file_dict:
        spider = Spider(SAVE_PATH, 2, local_file_list=file_dict)
    else:
        spider = Spider(SAVE_PATH, 2)

    spider.set_path()
    spider.get_dlink_type_list()
    spider.print_dlink_list()
    spider.get_dlink_list_len()
    spider.set_dlink_info()
    spider.get_all_file()


def test_spider_run():
    t = TraverFile(SAVE_PATH)
    t.find_already_firmware()
    file_dict = t.get_filepath()

    print(file_dict)
    if file_dict:
        spider = Spider(SAVE_PATH, 2, local_file_list=file_dict)
    else:
        spider = Spider(SAVE_PATH, 2)

    dlink_info_list = []
    dlink_info_list.append(Dlink_info(D_TYPE='DIR-859', D_REV=[], D_URLPATH='/PRODUCTS/DIR-859'))
    dlink_info_list.append(Dlink_info(D_TYPE='DIR-100', D_REV=['REVA'], D_URLPATH='/PRODUCTS/DIR-100'))
    dlink_info_list.append(Dlink_info(D_TYPE='DIR-816L', D_REV=['REVA', 'REVB'], D_URLPATH='/PRODUCTS/DIR-816L'))
    dlink_info_list.append(Dlink_info(D_TYPE='DIR-878', D_REV=['REVA'], D_URLPATH='/PRODUCTS/DIR-878'))
    spider.set_dlink_info_list(dlink_info_list)
    spider.get_all_file()


def main(h=00, m=54):
    em = Email()

    while True:
        now = datetime.datetime.now()
        # print(now.hour, now.minute)
        if now.hour == h and now.minute == m:
            em.send_mail(to="smile@smilehacker.net", sub="D-LINK SPIDER START",
                         content="datetime: {}   "
                                 "info: start number {}".format(now, RUNS.NUMBER_RUNS))
            test_spider_run()
            RUNS.add_number_runs()

            em.send_mail(to="smile@smilehacker.net", sub="D-LINK SPIDER END",
                         content="datetime: {}  "
                                 "info: start number {}".format(now, RUNS.NUMBER_RUNS))

        # 每隔60秒检测一次
        print("Wait RUN {}".format(datetime.datetime.now()))
        time.sleep(30)


if __name__ == "__main__":
    main()