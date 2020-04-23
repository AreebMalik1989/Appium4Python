#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import subprocess, time
from common.Log import *


class Server:

    def __init__(self, deviceobject):
        self.logger = Log.logger
        self._deviceobject = deviceobject
        self._cmd = "appium -p %s -bp %s -U %s --session-override" % (
                    self._deviceobject.server_port, self._deviceobject.bootstrap_port, self._deviceobject.device_id)

    def start(self):
        self.kill(self._deviceobject.server_port)
        time.sleep(3)
        info = "Start the device:%s Corresponding Appium Server" % self._deviceobject.device_name
        self.logger.info(info)
        self.logger.info(self._cmd)
        subprocess.call(self._cmd, shell=True)

    def stop(self):
        self.kill(self._deviceobject.server_port)

    def kill(self, port):
        cmd = "lsof -i:%s|awk 'NR==2{print $2}'" % port
        self.logger.info(cmd)
        pid = os.popen(cmd).read()
        cmd = "kill -9 %s" % pid
        os.popen(cmd).read()

    def list_connect_devices(self):
        info = "Connected devices： %s ------ %s" % (self._deviceobject.device_id, self._deviceobject.device_name)
        self.logger.info(info)

    def list_disconnect_devices(self):
        info = "！！！Device lost！！！： %s ------ %s" % (self._deviceobject.device_id, self._deviceobject.device_name)
        self.logger.info(info)
