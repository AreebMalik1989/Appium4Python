#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import threading
from common.DeviceManager import *
from .Server import *


class ServerManager:

    def __init__(self):
        self.test_devices = DeviceManager.test_devices
        self.disconnect_devices = DeviceManager.disconnect_devices
        self.server_objects = []
        self.threads = []
        self.logger = Log.logger

    def start_all_server(self):
        for device_id, device in self.test_devices.iteritems():
            server = Server(device)
            self.server_objects.append(server)
            t = threading.Thread(target=server.start)
            t.start()

    def stop_all_server(self):
        for server in self.server_objects:
            server.stop()

    def list_devices(self):
        info = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Connected devices~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        self.logger.info(info)
        for device_id, device in self.test_devices.iteritems():
            server = Server(device)
            server.list_connect_devices()
        info = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        self.logger.info(info)

    def list_disconnect_devices(self):
        info = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Lost device~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        self.logger.info(info)
        for device_id, device in self.disconnect_devices.iteritems():
            server = Server(device)
            server.list_disconnect_devices()
        info = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        self.logger.info(info)
