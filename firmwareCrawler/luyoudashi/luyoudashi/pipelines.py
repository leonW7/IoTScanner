# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import MySQLdb
import MySQLdb.cursors
from urllib import parse
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy.pipelines.files import FilesPipeline
from twisted.enterprise import adbapi


class DownloadPipeline(FilesPipeline):

    @classmethod
    def from_settings(cls, settings):
        # 此方法用于加载配置文件
        store_uri = settings['FILES_STORE']
        cls.expires = settings.getint('FILES_EXPIRES')
        cls.files_urls_field = settings.get('FILES_URLS_FIELD')
        cls.files_result_field = settings.get('FILES_RESULT_FIELD')

        return cls(store_uri, settings=settings)

    def file_path(self, request, response=None, info=None):
        # 此方法是用于重命名文件名的
        # extension = os.path.splitext(os.path.basename(
        #     parse.urlsplit(request.url).path))[1]
        # return "%s/%s%s" % (request.meta["vendor"],
        #                     hashlib.sha1(request.url).hexdigest(), extension)
        # print("%s/%s" % (request.meta["vendor"], request.url.split("/")[-1]))
        return "%s/%s" % (request.meta["vendor"], request.url.split("/")[-1])

    def get_media_requests(self, item, info):
        for x in ["vendor", "url"]:
            if x not in item:
                raise DropItem(
                    "Missing required field '%s' for item: " % (x, item))

        url = parse.urlparse(item["url"])
        if any(url.path.endswith(x) for x in
               [".pdf", ".php", ".txt", ".doc", ".rtf", ".docx", ".htm", ".html", ".md5", ".sha1", ".torrent"]):
            raise DropItem("Filtered path extension: %s" % url.path)
        elif any(x in url.path for x in ["driver", "utility", "install", "wizard", "gpl", "login"]):
            raise DropItem("Filtered path type: %s" % url.path)

        for file_url in item['file_urls']:
            yield Request(file_url, meta={"vendor":item["vendor"]})

    def item_completed(self, results, item, info):
        for ok, value in results:
            if ok:
                item["filename"] = value["path"]
                item["checksum"] = value["checksum"]
        return item


class MysqlTwistedPipeline(object):
    """
    Mysql异步插入机制
    """
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行

        query = self.dbpool.runInteraction(self.do_insert, item)

        query.addErrback(self.handle_error, item)  # 处理异常

    def handle_error(self, failure, item):
        # 处理异步插入的异常
        if failure:
            print(failure)

    def do_insert(self, cursor, item):
        info = cursor.execute(
            "INSERT INTO info(product_detail_url, vendor, source, adapter, version, size, release_time, version_description, url, filename, checksum) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE "
            "vendor=VALUES(vendor), source=VALUES(source),"
            "adapter=VALUES(adapter), version_description=VALUES(version_description),"
            "url=VALUES(url), filename=VALUES(filename)"
            ,
            (
                item["product_detail_url"],
                item["vendor"],
                item["source"],
                item["adapter"],
                item["version"],
                item["size"],
                item["release_time"],
                item["version_description"],
                item["url"],
                item["filename"],
                item["checksum"],
            )
        )