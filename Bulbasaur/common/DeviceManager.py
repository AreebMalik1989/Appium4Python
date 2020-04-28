#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from .DataProvider import *
from .Log import *


class DeviceManager:

    # Connected device ID
    connect_device_id = []

    # Device object to be tested
    test_devices = {}

    # Equipment with established service
    server_devices = {}

    # Unconnected devices in the device library
    disconnect_devices = {}

    # Connected device IMEI
    connect_imei = []

    logger = None

    @classmethod
    def get_connect_device_id(cls):
        p = os.popen('adb devices')
        out_str = p.read()
        cls.connect_device_id = re.findall(r'(\w+)\s+device\s', out_str)
        if len(cls.connect_device_id) == 0:
            Log.logger.warn('device without adb connection')
        else:
            return cls.connect_device_id

    # Server is used to obtain the linked server
    @classmethod
    def get_test_device(cls):
        for device_id in cls.connect_device_id:
            if device_id in DataProvider.devices.keys():
                cls.test_devices[device_id] = DataProvider.devices[device_id]
            else:
                Log.logger.warn('device: %s is not in the configuration list ' % device_id)
        if len(cls.test_devices) == 0:
            Log.logger.warn('no device to be tested')

    # The client is used to obtain the equipment that has been established on the server
    @classmethod
    def get_server_test_device(cls):
        for device_id, device in DataProvider.devices.iteritems():
            url = "http://%s:%s/wd/hub" % (device.server, device.serverport)
            response = None
            try:
                response = requests.request("get", url)
            except requests.RequestException as e:
                print(e)
            if response:
                cls.server_devices[device_id] = device
            else:
                cls.disconnect_devices[device_id] = device

    @classmethod
    def get_connect_device_imei(cls):
        for device in cls.connect_device_id:
            cmd = "adb -s %s shell service call iphonesubinfo 1 | awk -F \"'\" '{print $2}' | sed '1 d' | " \
                  "tr -d '.' | awk '{print}' ORS=" % device
            p = os.popen(cmd)
            out_str = p.read()
            print(device)
            print(out_str)

    @classmethod
    def get_device_info(cls, device_id):
        mode = "ro.product.model"
        release = "ro.build.version.release"
        get_mode = "adb -s %s shell cat /system/build.prop |grep %s" % (device_id, mode)
        get_release = "adb -s %s shell cat /system/build.prop |grep %s" % (device_id, release)
        p1 = os.popen(get_mode)
        p2 = os.popen(get_release)
        mode_name = p1.read()
        release_name = p2.read()
        print(device_id)
        print(mode_name, release_name)


if __name__ == "__main__":
    DeviceManager.get_connect_device_id()
