#!usr/bin/python
# -*- coding:utf-8 -*-

from .BaseDevicePreProcess import *
import subprocess
from common.DataProvider import *


class M57APreProcess(BaseDevicePreProcess):

    def __init__(self, tester):
        super(M57APreProcess, self).__init__(tester)

    # Meizu situation is too special, the installation must be inherited and processed separately, the pop-up adb
    # installation permission directly blocks the server operation
    def install_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.device_id, DataProvider.niceapk)
        subprocess.call(cmd, shell=True)

    def install_process(self):
        try:
            Log.logger.info("Device: %s install app and handle GPS popup" % self.tester.device.device_name)

            # adbInstallation permissions
            self.tester.find_element_by_id_and_tap('android:id/button1')

            # Start app
            while not self.driver.is_app_installed("com.nice.main"):
                time.sleep(2)
            self.driver.launch_app()

            # GPS permissions
            # self.tester.find_element_by_id_and_tap('android:id/button1')

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def login_success_process(self):
        try:
            Log.logger.info("Device: %s After successful login, process various automatic pop-up windows" % self.tester.device.device_name)

            # Contact permissions
            # self.tester.find_element_by_id_and_tap('android:id/button1')

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def get_permission_process(self):
        try:
            Log.logger.info("Device:% s Get camera and recording permissions" % self.tester.device.device_name)

            # Open the viewfinder
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            # Recording permissions
            # self.tester.find_element_by_id_and_tap('android:id/button1')

            # Close the viewfinder
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)
