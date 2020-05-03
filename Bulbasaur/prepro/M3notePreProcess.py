#!usr/bin/python
# -*- coding:utf-8 -*-

from .BaseDevicePreProcess import *
import subprocess
from common.DataProvider import *


class M3notePreProcess(BaseDevicePreProcess):

    def __init__(self, tester):
        super(M3notePreProcess, self).__init__(tester)

    # Meizu situation is too special, the installation must be inherited and processed separately, the pop-up adb
    # installation permission directly blocks the server operation
    def install_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.device_id, DataProvider.niceapk)
        subprocess.call(cmd, shell=True)

    def install_process(self):

        Log.logger.info("Device: %s install app and handle GPS popup" % self.tester.device.device_name)
        try:
            # adb
            element = self.tester.find_element_by_id("android:id/button1", 20)
            if element is not None:
                self.action.tap(element).perform()

            # Launch app
            while not self.driver.is_app_installed("com.nice.main"):
                time.sleep(2)
            self.driver.launch_app()

            # nice get mobile phone GPS permission
            element = self.tester.find_element_by_id("android:id/button1", 20)
            if element is not None:
                self.action.tap(element).perform()

            # nice Get phone identification code permissions
            element = self.tester.find_element_by_id("android:id/button1", 10)
            if element is not None:
                self.action.tap(element).perform()

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def login_process(self):
        Log.logger.info("device: %s to start logging in, using account:% s" % (
            self.tester.device.device_name, self.tester.user.mobile))
        try:
            # The login button of the new and old registration process uses the same resource_id, no special judgment
            # is required for the login button

            # First get the login button object of the registration page
            register_login_element = self.tester.find_element_by_id('com.nice.main:id/login')

            # Click to Login
            self.action.tap(register_login_element).perform()

            time.sleep(2)

            login_phone_number_element = self.tester.find_element_by_id('com.nice.main:id/phone_number', 2)
            while login_phone_number_element is None:
                self.action.tap(register_login_element).perform()
                time.sleep(2)
                login_phone_number_element = self.tester.find_element_by_id('com.nice.main:id/phone_number', 2)

            # Enter account password
            login_phone_number_element.send_keys(self.user.mobile)
            login_password = self.tester.find_element_by_id('com.nice.main:id/password')
            self.action.tap(login_password).perform()
            login_password.send_keys(self.user.password)

            # Judgment until the login is successful
            self.tester.find_element_by_id_and_tap('com.nice.main:id/login')
            time.sleep(5)
            self.tester.screenshot("Login successful")
        except Exception as e:
            raise

    def login_success_process(self):
        try:
            Log.logger.info(
                "Device: %s After successful login, process various automatic pop-up windows" % self.tester.device.device_name)

            # Contact permissions
            self.tester.find_element_by_id_and_tap('android:id/button1')

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def get_permission_process(self):
        try:
            Log.logger.info("Device: %s Get camera and recording permissions" % self.tester.device.device_name)

            # Open the viewfinder
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            # Address book permissions
            self.tester.find_element_by_id_and_tap('android:id/button1')
            # Recording authority
            time.sleep(2)
            self.tester.find_element_by_id_and_tap('android:id/button1')

            # Close the viewfinder
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)
