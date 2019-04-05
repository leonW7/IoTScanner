# -*- coding: utf-8 -*-
# @File  : general.py
# @Author: TT
# @Email : tt.jiaqi@gmail.com
# @Date  : 2018/12/4
# @Desc  : some comments functions
import re
from copy import deepcopy

def getchromdriver_version():
    """
    使用获取到的系统信息来设置chromdriver的版本
    :return:
    """
    import platform
    system_info = platform.system()
    if system_info == "Windows":
        return "chromedriver.exe"
    elif system_info == "Linux":
        return "chromedriver"
    else:
        exit(0)


def size_cover(size):
    com = size.split(' ')[1]
    size = float(size.split(' ')[0])
    if com == "MB":
        if size >= 1.0:
            return True
        else:
            return False
    else:
        return False


def download_rule(all_firmware):
    all_firmware_back = deepcopy(all_firmware)
    max_version = 0.0
    max_version_key = ""
    pattern = re.compile("(v[\d]{1}.[\d]{2})")
    for firmware in all_firmware.keys():
        firmware_list = firmware.split(" ")
        for str in firmware_list:
            version = pattern.findall(str)
            if version:
                ver = float(version[0].replace("v", ""))
                if max_version != 0.0:
                    if ver > max_version:
                        max_version = ver
                        max_version_key = firmware
                        all_firmware_back.pop(max_version_key)
                    else:
                        all_firmware_back.pop(firmware)
                else:
                    max_version = ver
                    max_version_key = firmware
                    continue

    for i in all_firmware_back.values():
        return i


if __name__ == "__main__":
    dict = {'Firmware: DIR-816L B1 v2.06ES for DSG': "dwn('NOISNWHWNQ','1')", 'Firmware: DIR-816L A1 v1.00': "dwn('CDLKAIFI','1')", 'Firmware: DIR-816L A1 v1.01': "dwn('BCEHIEHCDF','1')", 'Firmware: DIR-816L B1 v2.00': "dwn('HOBPGL','1')", 'Firmware: DIR-816L B1 v2.01 for WW': "dwn('KLDNDTMQ','1')", 'Firmware: DIR-816L B1 v2.02 for WW': "dwn('FNINEH','1')", 'Firmware: DIR-816L B1 v2.03 for WW': "dwn('NSETLW','1')", 'Firmware: DIR-816L B1 v2.04 for WW': "dwn('JKGMHONNBJ','1')", 'Firmware: DIR-816L B1 v2.05 for WW': "dwn('JKJNLPJONN','1')", 'Firmware: DIR-816L B1 v2.06 for WW': "dwn('IJBOEJDLEK','1')"}
    a = download_rule(dict)
    print(a)