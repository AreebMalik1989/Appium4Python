#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from common.DeviceManager import *
from common.DataProvider import *
import sys
from Server.ServerManager import ServerManager


def run():
    # Initialize log configuration
    Log.create_log_file()

    Log.logger.info("Load device and user configuration information")
    DataProvider.init_data()

    Log.logger.info("ADB connected device")
    DeviceManager.get_connect_device_id()

    if len(DeviceManager.connect_device_id) == 0:
        Log.logger.info("No connected device")
        sys.exit()
    else:
        Log.logger.info("Number of currently connected devices: %s" % len(DeviceManager.connect_device_id))

    Log.logger.info("Get the device to be tested")
    DeviceManager.get_test_device()
    DeviceManager.get_server_test_device()

    server_manager = ServerManager()
    server_manager.list_devices()

    if len(DeviceManager.disconnect_devices) > 0:
        Log.logger.info("Lost backup: %s" % len(DeviceManager.disconnect_devices))

    server_manager.list_disconnect_devices()
    server_manager.start_all_server()


if __name__ == "__main__":
    run()
