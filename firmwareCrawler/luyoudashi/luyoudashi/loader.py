#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 2019/12/12 14:20 
# @Author : TT
# @Site :  
# @File : loader.py.py 
# @Software: PyCharm

from scrapy.loader.processors import TakeFirst
from scrapy.loader import ItemLoader


class LuyoudashiItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
