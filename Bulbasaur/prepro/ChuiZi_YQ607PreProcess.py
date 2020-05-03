#!usr/bin/python
# -*- coding:utf-8 -*-

from .BaseDevicePreProcess import *
import subprocess
from common.DataProvider import *


class ChuiZi_YQ607PreProcess(BaseDevicePreProcess):

    def __init__(self, tester):
        super(ChuiZi_YQ607PreProcess, self).__init__(tester)

    def install_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.device_id, DataProvider.niceapk)
        subprocess.call(cmd, shell=True)

    def install_process(self):
        try:
            Log.logger.info("Device: %s install app and handle GPS popup" % self.tester.device.device_name)

            # Start app
            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)
            self.driver.launch_app()

            # Get location information
            time.sleep(5)
            self.tester.find_element_by_id_and_tap('android:id/button1')

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)
            # The process includes clicking the login button to reach the login page and log in

    def login_process(self):
        Log.logger.info("device: %s to start logging in, using account:% s" % (
        self.tester.device.device_name, self.tester.user.mobile))
        try:
            # The login button of the new and old registration process uses the same resource_id, no special judgment is required for the login button
            self.tester.find_element_by_id_and_tap('com.nice.main:id/login')
            self.tester.find_element_by_id_and_send_keys('com.nice.main:id/phone_number', self.user.mobile)
            self.tester.find_element_by_id_and_tap('com.nice.main:id/password')
            self.tester.find_element_by_id_and_send_keys('com.nice.main:id/password', self.user.password)
            self.tester.find_element_by_id_and_tap('com.nice.main:id/login')

            time.sleep(1)
            self.tester.screenshot("Login successful")
        except Exception as e:
            raise

    def login_success_process(self):
        try:
            Log.logger.info(
                "Device: %s After successful login, process various automatic pop-up windows" % self.tester.device.device_name)

            element = self.tester.find_element_by_id("android:id/button1")
            if element is not None:
                self.action.tap(element).perform()

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def get_permission_process(self):
        try:
            Log.logger.info("Device: %s Get camera and recording permissions" % self.tester.device.device_name)

            # Open the viewfinder
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            time.sleep(3)
            # Permissions
            self.tester.find_element_by_id_and_tap('android:id/button1')

            # Permissions
            self.tester.find_element_by_id_and_tap('android:id/button1')

            # Close the viewfinder
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)
