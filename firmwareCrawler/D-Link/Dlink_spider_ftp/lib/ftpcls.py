# -*- coding: utf-8 -*-
# @File     : ftpcls.py
# @Author   : TT
# @Email    : tt.jiaqi@gmail.com
# @Date     : 19-2-12 上午11:09
# @Desc     :

from ftplib import FTP


class Ftpcls(FTP):

    def getSubdir(self, *args):
        '''拷贝了 nlst() 和 dir() 代码修改，返回详细信息而不打印'''
        cmd = 'LIST'
        func = None
        if args[-1:] and type(args[-1]) != type(''):
            args, func = args[:-1], args[-1]
        for arg in args:
            cmd = cmd + (' ' + arg)
        files = []
        self.retrlines(cmd, files.append)
        return files

    def getdirs(self, dirname=None):
        """返回目录列表，包括文件简要信息"""
        if dirname != None:
            self.cwd(dirname)
        files = self.getSubdir()

        # 处理返回结果，只需要目录名称
        r_files = [file.split(" ")[-1] for file in files]

        # 去除. ..
        return [file for file in r_files if file != "." and file != ".."]

    def getfiles(self, dirname=None):
        """返回文件列表，简要信息"""
        if dirname != None:
            self.cwd(dirname)  # 设置FTP当前操作的路径
        return self.nlst()  # 获取目录下的文件
