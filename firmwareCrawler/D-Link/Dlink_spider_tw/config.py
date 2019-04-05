# -*- coding: utf-8 -*-
# @File  : config.py
# @Author: TT
# @Email : tt.jiaqi@gmail.com
# @Date  : 2018/12/4
# @Desc  : config file
from utils.general import getchromdriver_version
from chromedriver.path import path
import os
import sys

chromedriver = os.path.abspath(os.path.dirname(__file__)) + "\\chromedriver\\"+ getchromdriver_version()

download_path = os.path.abspath(os.path.dirname(__file__)) + "\\"

Suffix_name = ['.bin', '.rar', '.zip', '.7z']
