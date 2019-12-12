#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 2019/12/12 11:26 
# @Author : TT
# @Site :  
# @File : main.py 
# @Software: PyCharm

from scrapy.cmdline import execute

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "luyoudashi"])