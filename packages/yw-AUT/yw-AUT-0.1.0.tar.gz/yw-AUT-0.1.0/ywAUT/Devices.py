#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ATX_Server, get devices, connect devices
Author: 韩杰峰
"""

import logging

from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage
import requests
import re
import uiautomator2 as u2
import subprocess
from ReadConfig import ReadConfig

logger = logging.getLogger(__name__)

TinyDB.DEFAULT_STORAGE = MemoryStorage


class ATX_Server(object):
    """
    According to users requirements to select devices
    """

    def __init__(self, url):
        """
        Construct method
        """
        self._db = TinyDB(storage=MemoryStorage)
        if url and re.match(r"(http://)?(\d+\.\d+\.\d+\.\d+:\d+)", url):
            if '://' not in url:
                url = 'http://' + url + '/list'
            else:
                url = url + '/list'
            self._url = url
            self.load()
        else:
            logger.error('Atx server addr error')
        self.load()

    def load(self):
        """
        Use the data which got from stf platform to crate query db

        :return: the len of records in the db's table
        """
        res = requests.get(self._url).json()
        if res is not None:
            eids = self._db.insert_multiple(res)
            return len(eids)
        else:
            return 0

    def find(self, cond=None):
        """
        According condition to filter devices and return
        :param cond: condition to filter devices
        :type cond: where
        :return: stf_selector object and its db contains devices
        """
        if cond is not None:
            res = self._db.search(cond)
            self.purge()
            self._db.insert_multiple(res)
        return self

    def devices(self):
        """
        return all devices that meeting the requirement
        :return: list of devices
        """
        return self._db.all()

    def refresh(self):
        """
        reload the devices info from stf
        :return: the len of records in the db's table
        """
        self.purge()
        return self.load()

    def count(self):
        """
        count the records in the db's table
        :return: the len of records in the db's table
        """
        return len(self._db.all())

    def purge(self):
        """
        remove all the data from the db
        :return:
        """
        self._db.purge()

    def ready_devices(self):
        """查找标记为ready的设备"""
        self.refresh()
        devices = self.find(where('ready') == True).devices()
        if len(devices) > 0:
            return devices
        else:
            return False

    def online_devices(self):
        """查找online 的设备"""
        self.refresh()
        devices = self.find(where('present') == True).devices()
        if len(devices) > 0:
            return devices
        else:
            return False

    def model_devices(self, model):
        """查找特定型号的设备"""
        self.refresh()
        devices = self.find(where('model') == model).devices()
        if len(devices) > 0:
            return devices
        else:
            return False

    def brand_devices(self, brand):
        """查找特定品牌的设备"""
        self.refresh()

        devices = self.find(where('brand') == brand).devices()
        if len(devices) > 0:
            return devices
        else:
            return False

    def sdk_devices(self, sdk):
        '''查找特定SDK的设备'''
        self.refresh()
        devices = self.find(where('sdk') == sdk).devices()
        if len(devices) > 0:
            return devices
        else:
            return False

    def version_devices(self, version):
        '''查找特定SDK的设备'''
        self.refresh()
        devices = self.find(where('version') == version).devices()
        if len(devices) > 0:
            return devices
        else:
            return False

    def serial_devices(self, serial):
        '''查找特定serial的设备'''
        self.refresh()
        devices = self.find(where('serial') == serial).devices()
        if len(devices) > 0:
            return devices
        else:
            return False

    def all_devices(self):
        '''返回所有的设备'''
        self.refresh()
        devices = self.find().devices()
        if len(devices) > 0:
            return devices
        else:
            return False



'''
连接config.ini中指定IP设备
'''


def get_devices_config_ip():
    """get the devices from Pubilc/config.ini devices list
    return alive devices"""
    devices_ip = ReadConfig().get_devices_ip()
    print('连接设备平台中指定设备，IP： %s' % devices_ip)
    devices_list = []
    for i in devices_ip:
        try:
            device = u2.connect(i)
            if device.alive:
                dict_tmp = device.device_info
                dict_tmp['ip'] = i
                devices_list.append(dict_tmp)
            else:
                print('The IP %s device is not alive,please checkout!' % i)
        except Exception as e:
            print('Raise ERROR %s\nThe IP %s device is not alive,please checkout!' % (e, i))
    return device

'''
连接server设备列表中中第一个online设备
'''


def connect_devices_online_ip(devices_ip):
    """connect the devices from at-server devices list
    return alive devices"""
    print('连接设备平台中首个在线设备，IP： %s' % devices_ip)
    devices_list = []
    try:
        device = u2.connect(devices_ip)
        if device.alive:
            dict_tmp = device.device_info
            dict_tmp['ip'] = devices_ip
            devices_list.append(dict_tmp)
        else:
            print('The IP %s device is not alive,please checkout!' % devices_ip)
    except Exception as e:
        print('Raise ERROR %s\nThe IP %s device is not alive,please checkout!' % (e, devices_ip))
    return device


'''
连接已插线设备
'''


def connect_usb_devices():
    '''get the devices usb connected on PC
    return alive devices'''
    output = subprocess.check_output(['adb', 'devices'])
    pattern = re.compile(
        r'(?P<serial>[^\s]+)\t(?P<status>device|offline)')
    matches = pattern.findall(output.decode())
    valid_serials = [m[0] for m in matches if m[1] == 'device']

    if valid_serials:
        print('连接USB设备，设备名 %s' % valid_serials)
        devices_list = []
        for i in valid_serials:
            try:
                device = u2.connect_usb(i)
                # device.healthcheck()
                if device.alive:
                    dict_tmp = device.device_info
                    devices_list.append(dict_tmp)
                else:
                    print('The serial %s device is not alive,please checkout!' % i)
            except Exception as e:
                print('Raise ERROR %s\nThe serial %s device is not alive,please checkout!' % (e, i))
        return device
    if len(valid_serials) == 0:
        print("未发现可用的USB设备,请检查设备连接情况!")


if __name__ == '__main__':
        # # get device
    #s from atx-server
    s = ATX_Server('http://10.97.190.152:7100/api/v1/devices')
    print(s.devices())
    print(s.online_devices())
    # print(s.ready_devices())
    #
    #     # get devices from config.ini devices list
    #print(get_devices())
    #print(connect_devices_online_ip(s.online_devices()[0]['ip']))
