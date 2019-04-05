# -*- coding: utf-8 -*-
# @File     : spider.py
# @Author   : TT
# @Email    : tt.jiaqi@gmail.com
# @Date     : 19-2-12 上午10:59
# @Desc     : From ftp://ftp2.dlink.com/ download dlink firmware

from .ftpcls import Ftpcls
from .config import SAVE_PATH, NEED_TYPE, DOWNLOAD_GPL
from .general import RUNS, exec_command
from .mail import Email

import ftplib
import copy
import os


class Dlink_info(object):

    def __init__(self, D_TYPE=None, D_REV=None, D_URLPATH=None):
        self.D_FILE_DICT = None #生成输出日志时使用
        self.HAVE_GPL = None

        '''

        :param D_TYPE:  路由器种类
        :param D_REV:   路由器的架构  【列表】
        :param D_URLPATH: 路由器存放路径
        '''
        self.D_TYPE = D_TYPE
        self.D_REV = D_REV
        self.D_URLPATH = D_URLPATH
        self.HAVE_GPL_LIST = []

    def set_D_TYPE(self, D_TYPE):
        self.D_TYPE = D_TYPE

    def set_D_REV(self, D_REV):
        self.D_REV = D_REV

    def set_D_URLPATH(self, D_URLPATH):
        self.D_URLPATH = D_URLPATH

    def set_D_FILE_DICT(self, D_FILE_DICT):
        """

        :param D_FILE_DICT: {REVA : [AAAA, BBBB, CCCC], REVB : [AAAA,BBBB,CCCC]}
        :return:
        """
        self.D_FILE_DICT = D_FILE_DICT

    def set_HAVE_GPL(self, GPL_TYPE):
        """
        HAVE_GPL_LIST :[REVA, REVB] 列表中的元素说明存在GPL
        :param GPL_TYPE: 存在GPL的型号
        :return:
        """
        self.HAVE_GPL_LIST.append(GPL_TYPE)

    def print_D_FILE_DICT(self):
        print(self.D_FILE_DICT)


class Spider(object):

    def __init__(self, savepath, debug_level, local_file_list={}):
        self.dlink_type_list = []   # D-Link全部产品列表
        self.dlink_list = []        # 需要的型号
        self.dlink_info_list = []   # 用来存放dlink_info的nametuple
        self.continue_ok = True

        self.local_file_list = local_file_list   # 本地文件列表   已经下载到本地的文件

        self.savepath = savepath
        self.ftp = Ftpcls()
        self.ftp.set_debuglevel(debug_level)
        try:
            self.ftp.connect('ftp2.dlink.com', 21)
            self.ftp.login('anonymous', '')
        except Exception as e:
            em = Email()
            em.send_mail("smilehacker.net", "Login connect Exception", e)

        self.em = Email()
        print(self.ftp.getwelcome())

    # def __del__(self):
    #
    #     self.ftp.close()
    #     print("已关闭ftp连接")
    #     self.ftp.quit()

    def set_path(self, path="PRODUCTS"):
        self.ftp.cwd(path)

    def get_dlink_type_list(self):
        self.dlink_type_list = self.ftp.getdirs()
        for _type in self.dlink_type_list:
            for _need in NEED_TYPE:
                if _type.lower().startswith(_need.lower()):
                    self.dlink_list.append(_type)
                    break

    def set_dlink_info(self):
        for dlink in self.dlink_list:
            # if dlink != "DIR-859":
            #     continue
            dlink_type = dlink
            dlink_urlpath = "/PRODUCTS/"+dlink
            dlink_REV = self.ftp.getdirs(dlink_urlpath)
            _file = self.ftp.getfiles(dlink_urlpath)
            if [_ for _ in dlink_REV if _.lower().endswith('zip') or _.lower().endswith('pdf')] != []:
                # TODO 执行下载方法:(这里下载的是没有区分A B架构的)
                #self.judje_download(dlink_type, _file, dlink_urlpath)

                # 没必要添加进Dlink_info 直接下载即可
                self.dlink_info_list.append(Dlink_info(dlink_type, [], dlink_urlpath))
            else:
                self.dlink_info_list.append(Dlink_info(dlink_type, dlink_REV, dlink_urlpath))


    def get_all_file(self):
        for dlink in self.dlink_info_list:
            # if dlink.D_TYPE != "DIR-859":
            #     continue
            _info_dict = {}
            if dlink.D_REV != []:
                for _rev in dlink.D_REV:
                    _path = dlink.D_URLPATH + "/" + _rev
                    _file = self.ftp.getfiles(_path)
                    if [ _ for _ in _file if _.lower().endswith('zip') or _.lower().endswith('pdf')] != []:
                        # TODO  遍历`_file`开始下载文件(有区分A B架构),如果名称为GPL,说明存在此架构型号的路由器存在可下载的符号表
                        self.judje_download(dlink, _file, _path)

                    _info_dict[_rev] = _file
                dlink.set_D_FILE_DICT(_info_dict)
            else:
                _path = dlink.D_URLPATH
                _file = self.ftp.getfiles(_path)
                if [_ for _ in _file if _.lower().endswith('zip') or _.lower().endswith('pdf')] != []:
                    # TODO  遍历`_file`开始下载文件(有区分A B架构),如果名称为GPL,说明存在此架构型号的路由器存在可下载的符号表
                    self.judje_download(dlink, _file, _path)
                    _info_dict["NOT_REV"] = _file
                dlink.set_D_FILE_DICT(_info_dict)
            pass

    def judje_download(self, dlink_type, _file, dlink_urlpath):
        D = False

        for _f in _file:
            D = True
            self.continue_ok = True
            if _f.lower().endswith('pdf') or _f.lower().endswith('txt'):
                continue

            if _f == "GPL":

                if DOWNLOAD_GPL:
                    url_path = dlink_urlpath + "/" + "GPL"

                    this_file = self.ftp.getfiles(url_path)
                    self.judje_download(this_file, url_path)

                else:
                    continue

            if Spider.checkFileDir(self.ftp, _f):
                #防止有其他文件夹程序崩溃
                continue

            print(self.local_file_list.get(dlink_type.D_TYPE))
            if self.local_file_list.get(dlink_type.D_TYPE):
                for _fname in self.local_file_list[dlink_type.D_TYPE]:
                    if _fname == _f:
                        D = False
                        break

            if D:
                if RUNS.NUMBER_RUNS != 0:
                    self.em.send_mail(to="smile@smilehacker.net", sub="D-LINK SPIDER INFO",
                                 content="Discovery of new firmware {}".format(_f))
                while self.continue_ok:
                    self.download_file(dlink_urlpath + '/' + _f)
                    print("download file {0}".format(_f))

            else:
                continue

    def download_file(self, url):
        buffer_size = 1024 * 1024
        #write_file 拼接文件
        write_file = Spider.get_download_path(self.savepath, url)
        with open(write_file, "wb") as f:
            try:
                self.ftp.retrbinary('RETR {0}'.format(url), f.write, buffer_size)
                self.continue_ok = False
            except Exception as e:
                em = Email()
                em.send_mail("smile@smilehacker.net", "Download file {} Error".format(url), "{}".format(e))
                self.continue_ok = True
        if self.continue_ok:
            exec_command("rm -rf {}".format(write_file))


    @staticmethod
    def check_path_exis(path):
        # ???? 忘记要做什么了
        pass

    @staticmethod
    def get_download_path(savepath, url):

        _u = ""

        if savepath.endswith('/'):
            savepath = savepath[:-1]
        if url.startswith('/PRODUCTS/'):
            _u = url.replace('/PRODUCTS/', '/')

        path = savepath + _u
        path_list = path.split('/')
        path_end = '/'.join(path_list[:-1])

        if not os.path.exists(path_end):
            os.makedirs(path_end)

        if not os.path.exists(path):
            os.mknod(path)

        return path

    @staticmethod
    def checkFileDir(ftp, file_name):
        """
        判断当前目录下的文件与文件夹
        :param ftp: 实例化的FTP对象
        :param file_name: 文件名/文件夹名
        :return:   True / False 返回字符串“File”为文件，“Dir”问文件夹，“Unknow”为无法识别
        """
        rec = ""
        try:
            rec = ftp.cwd(file_name)  # 需要判断的元素
            ftp.cwd("..")  # 如果能通过路劲打开必为文件夹，在此返回上一级
        except ftplib.error_perm as fe:
            rec = fe  # 不能通过路劲打开必为文件，抓取其错误信息
        finally:
            if "550" in str(rec):
                # "File"
                return False
            elif "250" in str(rec):
                # "Dir"
                return True
            else:
                # "Unknow"
                return False

    def set_dlink_info_list(self, dlink_list):
        self.dlink_info_list = copy.deepcopy(dlink_list)

    def print_dlink_list(self):
        for i in self.dlink_list:
            print(i)

    def get_dlink_list_len(self):
        print(len(self.dlink_list))

    def set_dlink_list(self, dlink_list):
        self.dlink_list = copy.deepcopy(dlink_list)


if __name__ == "__main__":

    spider = Spider(SAVE_PATH, 2)
    # spider.set_path()
    # spider.get_dlink_type_list()
    # spider.print_dlink_list()
    # spider.get_dlink_list_len()
    # spider.set_dlink_info()

    spider.set_dlink_list(["DSR-SERIES", "DIR-859"])
    spider.set_dlink_info()

    dlink_info_list = []
    dlink_info_list.append(Dlink_info(D_TYPE='DIR-100', D_REV=['REVA'], D_URLPATH='/PRODUCTS/DIR-100'))
    dlink_info_list.append(Dlink_info(D_TYPE='DIR-816L', D_REV=['REVA', 'REVB'], D_URLPATH='/PRODUCTS/DIR-816L'))
    dlink_info_list.append(Dlink_info(D_TYPE='DIR-878', D_REV=['REVA'], D_URLPATH='/PRODUCTS/DIR-878'))
    spider.set_dlink_info_list(dlink_info_list)

    spider.get_all_file()
