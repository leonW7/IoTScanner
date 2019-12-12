# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst,MapCompose,Join,Identity


def get_vendor(value):
    if value:
        vendor = value.split(" ")[-1]
        if not vendor:
            return "D-Link"
        return vendor
    return value


def get_adapter(value):
    return value.split("适用机型： ")[-1].strip()


def get_version(value):
    return value.split("固件版本： ")[-1].strip()


def get_size(value):
    return value.split("文件大小： ")[-1].strip()


def get_release_time(value):
    return value.split("发布日期： ")[-1].strip()


def join_description(values):
    return Join(values)


class Join_list(object):

    def __call__(self, values):
        return " ".join(values)

class LuyoudashiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_detail_url = scrapy.Field()
    vendor = scrapy.Field(
        input_processor=MapCompose(get_vendor)
    )

    source = scrapy.Field()

    adapter = scrapy.Field(
        input_processor=MapCompose(get_adapter)
    )

    version = scrapy.Field(
        input_processor=MapCompose(get_version)
    )

    size = scrapy.Field(
        input_processor=MapCompose(get_size)
    )

    release_time = scrapy.Field(
        input_processor=MapCompose(get_release_time)
    )

    version_description = scrapy.Field(
        input_processor=Join_list()
    )

    url = scrapy.Field(
        # output_processor=Identity()
    )
    filename = scrapy.Field()
    checksum = scrapy.Field()

    # used by FilesPipeline
    files = scrapy.Field()
    file_urls = scrapy.Field(
        output_processor=Identity()
    )
