# -*- coding: utf-8 -*-
# @File  : run.py
# @Author: TT
# @Email : tt.jiaqi@gmail.com
# @Date  : 2019/4/6
# @Desc  : 

import requests
import sys
import os
import time

from xml.etree import ElementTree as ET
from scrapy.selector import Selector
from lib.config import SAVE_PATH
from lib.general import TraverFile
from concurrent import futures


ROUTE_INFO_LIST = []


class Route_info():
    def __init__(self, route_type, version, url):
        self.route_type = route_type
        self.version = version
        self.url = "http://support.netgear.cn" + url

        self.firmware_name = self.url.split('/')[-1]

    def __str__(self):
        return "路由器类型:{}\t固件版本:{}\t下载连接:{}".format(self.route_type,self.version,self.url)


def get_xml(url="http://support.netgear.cn/keySearch2.asp?keyword=R"):

    headers = {
        'Host': 'support.netgear.cn',
        'Referer': 'http://support.netgear.cn/download.asp',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.ConnectionError as e:
        print("Connect {} error! Please check your netword!".format(url))
        sys.exit(0)
    return response.text


def parse_xml(str_xml):
    type_url = ""
    type_name= ""
    type_dict = {}

    root =  ET.XML(str_xml)
    for _ in root.iter('message'):
        child_list = _.getchildren()
        for tree_one in child_list:
            if tree_one.tag == "text":
                type_name = tree_one.text
            if tree_one.tag == "linkurl":
                type_url = tree_one.text

        type_dict[type_name] = type_url

    return type_dict


def get_need_list(url_dict):
    """
    过滤出需要的固件类型
    如何过滤？

    for key in url_dict.keys():
        if key.startswith(""):
            pass
            # url_dict.pop(key)
        else:
            pass
    :param url_dict: {type : type_url}
    :return: url_dict
    """
    return url_dict


def get_details_url(url):
    headers = {
        'Host': 'support.netgear.cn',
        'Referer': 'http://support.netgear.cn/download.asp',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Content-Type': 'text/html; Charset=utf-8'
    }

    try:
        response = requests.get(url, headers=headers)
        response = response.text
    except requests.exceptions.ConnectionError as e:
        print("Connect {} error! Please check your netword!".format(url))
        response = ""
    return response


def get_download_url(type_name, response):
    global ROUTE_INFO_LIST
    download_selector = Selector(text=response)
    firm_selector = download_selector.css(".content table tbody tr")
    downloadurls = firm_selector.css(".linkblue a::attr(href)").extract()
    if downloadurls:
        for url in downloadurls:
            suffix = url.split(".")[-1]
            if suffix.lower() == "zip" or suffix.lower() == "img" or suffix.lower() == "chk" or suffix.lower() == "bin":
                version_href_url = url
                version_name = url.split("/")[-1]
                version_name = version_name.split("."+suffix)[0]
                ROUTE_INFO_LIST.append(Route_info(type_name,version_name,version_href_url))
            else:
                continue


def download_firmware(save_path, firmware_name, url):
    """
    download firmware
    :param firmware_name: router firmware name
    :param url: firmware download url
    :return:
    """
    savepath = save_path + "\\" + firmware_name
    print('%s\n --->>>\n  %s' % (url, savepath))
    startTime = time.time()

    headers = {
        'Host': 'support.netgear.cn',
        'Referer': 'http://support.netgear.cn/download.asp',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Content-Type': 'text/html; Charset=utf-8'
    }

    with requests.get(url, headers=headers, stream=True) as r:
        contentLength = int(r.headers['content-length'])
        line = 'content-length: %dB/ %.2fKB/ %.2fMB'
        line = line % (contentLength, contentLength / 1024, contentLength / 1024 / 1024)
        print(line)
        downSize = 0
        with open(savepath, 'wb') as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
                downSize += len(chunk)
                line = '%d KB/s - %.2f MB， 共 %.2f MB'
                line = line % (
                downSize / 1024 / (time.time() - startTime), downSize / 1024 / 1024, contentLength / 1024 / 1024)
                print(line, end='\r')
                if downSize >= contentLength:
                    break
        timeCost = time.time() - startTime
        line = '共耗时: %.2f s, 平均速度: %.2f KB/s'
        line = line % (timeCost, downSize / 1024 / timeCost)
        print(line)


if __name__ == "__main__":
    savepath = SAVE_PATH
    if not os.path.exists(savepath):
        os.makedirs(savepath)

    tf = TraverFile(SAVE_PATH)
    tf.find_already_firmware()
    files_dict = tf.get_filepath()

    base_url = "http://support.netgear.cn"
    wait_todo = []
    response = get_xml()
    type_dict = parse_xml(response)
    # 暂时不知道如何提取出产品信息， （R2000 为路由器还是网关设备）
    type_dict = get_need_list(type_dict)
    for key, value in type_dict.items():
        type_dict[key] = base_url + type_dict[key].replace("Detail", "More")

    for key, value in type_dict.items():
        print("key : {} \t value : {}".format(key, value))
        response = get_details_url(value)
        get_download_url(key, response)

    for route in ROUTE_INFO_LIST:
        print("{} {} {} {}".format(route.route_type, route.version, route.url, route.firmware_name))

    with futures.ThreadPoolExecutor(max_workers=10) as exector:
        for route in ROUTE_INFO_LIST:
            if route.firmware_name not in files_dict.get(route.route_type, []):
                savepath = SAVE_PATH + route.route_type.replace(' ', '_')

                if not os.path.exists(savepath):
                    os.makedirs(savepath)

                future = exector.submit(download_firmware, savepath, route.firmware_name, route.url)
                wait_todo.append(future)

        for future in futures.as_completed(wait_todo):
            future.result()