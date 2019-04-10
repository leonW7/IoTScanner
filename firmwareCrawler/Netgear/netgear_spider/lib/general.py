# -*- coding: utf-8 -*-
# @File  : general.py
# @Author: TT
# @Email : tt.jiaqi@gmail.com
# @Date  : 2019/4/9
# @Desc  :
import os
from lib.config import SAVE_PATH


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

        type_str = path.split('\\')[-1]
        return type_str


if __name__ == "__main__":
    a = TraverFile(SAVE_PATH)
    a.find_already_firmware()
    b = a.get_filepath()
    for key,value in b.items():
        print("key:{} value{}".format(key,value))