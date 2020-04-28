#!usr/bin/python
# -*- coding:utf-8 -*-

import yaml
from common.Log import *
from model.Device import *
from model.User import *


class DataProvider:

    users = []
    devices = {}
    config = None
    niceapk = ""
    unlockapk = os.getcwd() + "apk/unlock_apk-debug.apk"
    settingapk = os.getcwd() + "apk/settings_apk-debug.apk"
    imeapk = os.getcwd() + "apk/UnicodeIME-debug.apk"
    testers = {}
    start_time = {}
    stop_time = {}
    device_name_list = []

    @classmethod
    def init_data(cls):
        cls.init_config_yaml()
        cls.load_devices()
        cls.load_users()
        cls.load_others_config()
        cls.show_device_name_list()

    @classmethod
    def init_config_yaml(cls):
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + '/config/config.yaml'
        with open(file_path, 'r') as stream:
            try:
                cls.config = yaml.load(stream)
            except yaml.YAMLError as exc:
                print('Yaml read incorrectly')
                print(exc)

    @classmethod
    def load_devices(cls):
        cls.device_name_list = []
        for device in cls.config['Devices']:
            device_object = Device(device['deviceid'])
            device_object.device_name = device['devicename']
            device_object.server_port = device['serverport']
            device_object.bootstrap_port = device['bootstrapport']
            device_object.platform_name = device['platformname']
            device_object.platform_version = device['platformversion']
            device_object.server = device['server']
            cls.devices[device_object.device_id] = device_object
            cls.device_name_list.append(device['devicename'])
        Log.logger.info("There are %s devices in the configuration list" % len(cls.devices))

    @classmethod
    def load_users(cls):
        for user in cls.config['Users']:
            user_object = User(user['uid'])
            user_object.username = user['username']
            user_object.mobile = user['mobile']
            user_object.password = user['password']
            cls.users.append(user_object)
        Log.logger.info("There are %s user information in the configuration list" % len(cls.users))

    @classmethod
    def load_others_config(cls):
        if cls.config['NiceAPK']:
            cls.niceapk = cls.config['NiceAPK']

    @classmethod
    def show_device_name_list(cls):
        for i in range(len(cls.device_name_list)):
            if i % 10 == 0:
                print(cls.device_name_list[i] + ',')
            else:
                print(cls.device_name_list[i] + ',', i+1)
            i += 1


if __name__ == "__main__":
    DataProvider.init_data()
