# -*- coding: utf-8 -*-
# @File  : spider_run.py
# @Author: TT
# @Email : tt.jiaqi@gmail.com
# @Date  : 2018/12/4
# @Desc  : 
from src.chrome_oper import chromedriver_download_init
from selenium import webdriver
from config import chromedriver,Suffix_name
from scrapy.selector import Selector
from utils.general import size_cover, download_rule
import time
import re


Dlink_url_list = []


def spider_start():
    options = chromedriver_download_init("buzhongyao")
    browser = webdriver.Chrome(executable_path=chromedriver ,chrome_options=options)
    browser.get("https://tsd.dlink.com.tw/downloads2008list.asp?t=1&Category=Product%20Data%20II%3EWireless%20LAN%3EWireless%20router&pagetype=S")
    browser.find_element_by_css_selector(".td11 input[name='search_string']").send_keys("DIR")
    browser.find_element_by_css_selector(".td11 input[type='button']").click()
    while have_next(browser):
        browser.execute_script("go('N')")
    time.sleep(3)


def have_next(browser):
    a_selector = Selector(text=browser.page_source)
    have_n = a_selector.css("tr td[align='center'] table[width='100%'] tbody tr td[align='center'] a::text").extract()[-1]
    get_oMd(browser)
    if have_n == "Next":
        return True
    else:
        return False


def get_oMd(browser):
    t_selector = Selector(text=browser.page_source)
    dir_list = t_selector.css(".pord_listtd2 strong a::attr(href)").extract()
    for dlink_url in dir_list:
        dlink_url = dlink_url.replace("javascript:","")
        Dlink_url_list.append(dlink_url)


def have_firmware(html_str,browser):
    h_selector = Selector(text=html_str)
    have_f = h_selector.css("table[cellpadding='4'] tbody .td0").extract()
    currend_firmware_dict = {}
    for have in have_f:
        selector = Selector(text=have)
        type = selector.css("td[nowrap].MdDclist12:first-child::text").extract()[0]
        size = selector.css("td[align='right'].MdDclist12::text").extract()[0]
        desc_start = selector.css("td.MdDclist12::text").extract()[1]
        #在这里添加过滤条件
        if type == "Firmware" and size_cover(size) and desc_start.startswith('Firmware'):
            currend_firmware_dict[desc_start] = selector.css("tr::attr(onclick)").extract()[0]

    last_firmware = download_rule(currend_firmware_dict)
    browser.execute_script(last_firmware)
    get_download_url(browser,browser.page_source)


def get_download_url(browser,html_str):
    download_url_dict = {}
    selector = Selector(text=html_str)
    s = selector.css("table[bgcolor='#CCCCCC'] .MdDclist12 tbody tr td:nth-child(2)").extract()
    for i in s:
        i_selector = Selector(text=i)
        filename = i_selector.css("a::text").extract()[0]
        filename_script = i_selector.css("a::attr(href)").extract()[0].replace("javascript:","")
        download_url_dict[filename] = filename_script
    #print(download_url_dict)
    for key,value in download_url_dict.items():
        for suffix in Suffix_name:
            if key.endswith(suffix):
                browser.execute_script(value)
                time.sleep(10)
                break


def get_Dlink_firmware():
    pattern = re.compile("('.*,.*')")
    for dlink in Dlink_url_list:
        str_re1 = pattern.findall(dlink)[0].replace('\'', '').split(',')
        path = "-".join(str_re1)
        options, path = chromedriver_download_init(path)
        browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

        browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': path}}
        command_result = browser.execute("send_command", params)
        print(command_result)

        browser.get(
            "https://tsd.dlink.com.tw/downloads2008list.asp?t=1&Category=Product%20Data%20II%3EWireless%20LAN%3EWireless%20router&pagetype=S")
        browser.execute_script(dlink)
        html_str = browser.page_source
        have_firmware(html_str,browser)
        browser.quit()


if __name__ == "__main__":
    #spider_start()
    Dlink_url_list = [  "oMd('DIR','806')",
                        "oMd('DIR','808L')",
                        "oMd('DIR','809')",
                        "oMd('DIR','810L')",
                        "oMd('DIR','813')",
                        "oMd('DIR','814')",
                        "oMd('DIR','815')",
                        "oMd('DIR','816')",
                        "oMd('DIR','816L')"
                      ]
    get_Dlink_firmware()