# -*- coding: utf-8 -*-
# @File  : general.py
# @Author: TT
# @Email : tt.jiaqi@gmail.com
# @Date  : 2019/2/28
# @Desc  :
import os
from .config import SAVE_PATH, NEED_TYPE


class TraverFile(object):

    def __init__(self, dirname):

        self._dirname = dirname

        """
            self._filepath_dict = {"DIR-859" : ['DIR-859_REVA_FIRMWARE_1.03.B04.ZIP', 'DIR-859_REVA_FIRMWARE_v1.05B03.zip']}
        """
        self._filepath_dict = {}

    def find_already_firmware(self):
        self._alldir = os.walk(self._dirname)
        for file in self._alldir:

            if file[2] != []:
                type_str = self.get_type(file[0])
                if self._filepath_dict.get(type_str):
                    self._filepath_dict[type_str] = self._filepath_dict[type_str] + file[2]
                else:
                    self._filepath_dict[type_str] = file[2]

    def get_filepath(self):
        return self._filepath_dict

    def get_type(self, path):
        """
        从路径中提取出需要的型号:  config.py --> NEED_TYPE
        :param path: 文件路径
        :return: 字符型号
        """

        path_list = path.split('/')
        for str in path_list:
            for need in NEED_TYPE:
                if str.startswith(need):
                    return str

        return "UNKNOW"


class RUNS(object):
    """
    用来记录程序的运行次数
    """
    NUMBER_RUNS = 0

    @staticmethod
    def add_number_runs():
        RUNS.NUMBER_RUNS = RUNS.NUMBER_RUNS + 1


def exec_command(command):
    res = os.popen(command)
    res = res.read()
    return res


if __name__ == "__main__":
    t = TraverFile(SAVE_PATH)
    t.find_already_firmware()
    a = t.get_filepath()
    for key in a.keys():
        print(key)
        print(a[key])
