# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from luyoudashi.items import LuyoudashiItem
from luyoudashi.loader import LuyoudashiItemLoader


class BasicSpider(scrapy.Spider):
    name = 'luyoudashi'
    allowed_domains = ['luyoudashi.com']
    start_urls = ['http://www.luyoudashi.com/roms/vendor-13350.html',
                  'http://www.luyoudashi.com/roms/vendor-8080.html',
                  'http://www.luyoudashi.com/roms/vendor-4588.html',
                  'http://www.luyoudashi.com/roms/vendor-11367.html',
                  'http://www.luyoudashi.com/roms/vendor-12997.html',
                  'http://www.luyoudashi.com/roms/vendor-8806.html',
                  'http://www.luyoudashi.com/roms/vendor-8819.html',
                  'http://www.luyoudashi.com/roms/vendor-3132.html',
                  'http://www.luyoudashi.com/roms/vendor-14593.html',
                  'http://www.luyoudashi.com/roms/vendor-16501.html',
                  'http://www.luyoudashi.com/roms/vendor-16502.html',
                  'http://www.luyoudashi.com/roms/vendor-1130.html'
                  ]

    def parse(self, response):
        vendor = response.css(".left_menu .select a::text").extract_first()
        link = response.xpath("//div[@class='manu']/a[contains(@title,'下一页')]")
        if link:
            link = link.css("a::attr(href)").extract_first()
            yield Request(
                url=parse.urljoin(response.url, link),
                headers={"Referer": response.url},
                callback=self.parse
            )

        all_products = response.css(".r_info .rom_list ul li a::attr(href)").extract()
        for product_url in all_products:
            yield Request(
                url=parse.urljoin(response.url, product_url),
                meta={"vendor":vendor},
                headers={"Referer": response.url},
                callback=self.get_detail
            )

    def get_detail(self, response):
        detail_items = response.css(".rom_list_list li")
        for detail in detail_items:
            source = detail.css("span::text").extract_first()
            vendor = response.meta["vendor"]
            detail_url = detail.css("a::attr(href)").extract_first()
            yield Request(
                url=parse.urljoin(response.url, detail_url),
                meta={"vendor": vendor,
                      "source": source},
                headers={"Referer": response.url},
                callback=self.parse_detail
            )

    def parse_detail(self, response):
        item_loader = LuyoudashiItemLoader(item=LuyoudashiItem(),response=response)
        item_loader.add_value("product_detail_url", response.url)
        item_loader.add_value("vendor", response.meta["vendor"])
        item_loader.add_value("source", response.meta["source"])
        item_loader.add_xpath("adapter", "/html/body/div[3]/div[4]/div[1]/p[2]/text()")
        item_loader.add_xpath("version", "/html/body/div[3]/div[4]/div[1]/p[3]/text()")
        item_loader.add_xpath("size", "/html/body/div[3]/div[4]/div[1]/p[4]/text()")
        item_loader.add_xpath("release_time", "/html/body/div[3]/div[4]/div[1]/p[5]/text()")
        item_loader.add_css("version_description", ".rom_shuom::text")
        item_loader.add_css("url", ".f_r a.romdown::attr(href)")
        item_loader.add_css("file_urls", ".f_r a.romdown::attr(href)")
        luyoudashi_item = item_loader.load_item()

        yield luyoudashi_item