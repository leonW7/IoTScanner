# -*- coding: utf-8 -*-
# @File  : chrome_oper.py
# @Author: TT
# @Email : tt.jiaqi@gmail.com
# @Date  : 2018/12/4
# @Desc  : selenium operation chromedriver
from selenium import webdriver
from config import chromedriver, download_path
from selenium.webdriver.chrome.options import Options


def chromedriver_download_init(path):
    prefs = {'download.default_directory': download_path + "firmwarm\\" + path + "\\",
             "profile.managed_default_content_settings.images": 2,
             'safebrowsing.disable_download_protection': True,
             "download.prompt_for_download": False,
             "download.directory_upgrade": True,
             "safebrowsing.enabled": True
             }
    options = Options()
    options.add_experimental_option('prefs', prefs)
    return options, download_path + "firmwarm\\" + path + "\\"


if __name__ == "__main__":
    options = chromedriver_download_init("path_test")
    print(options)