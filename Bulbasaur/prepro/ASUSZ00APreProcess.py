#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from .BaseDevicePreProcess import *


class ASUSZ00APreProcessPreProcess(BaseDevicePreProcess):

    def __init__(self, tester):
        super(ASUSZ00APreProcessPreProcess, self).__init__(tester)

    def install_process(self):
        try:
            Log.logger.info("device：%s Launch app and handle GPS popup" % self.tester.device.device_name)

            while not self.driver.is_app_installed("com.nice.main"):
                time.sleep(2)

            self.driver.launch_app()

            # GPS permissions
            element = self.tester.find_element_by_id('android:id/button1')
            if element is not None:
                self.tester.tap_screen(155, 1065)
                self.action.tap(element).perform()

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def login_success_process(self):
        try:
            Log.logger.info("device：%s After successful login, handle various automatic pop-ups" % self.tester.device.device_name)

            # Contact permissions
            element = self.tester.find_element_by_id("android:id/button1")
            if element is not None:
                self.tester.tap_screen(191, 1063)
                self.action.tap(element).perform()

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def get_permission_process(self):
        Log.logger.info("device：%s Get camera and recording permissions" % self.tester.device.device_name)
        try:
            # Open the frame
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            # Camera permissions
            element = self.tester.find_element_by_id("android:id/button1")
            if element is not None:
                self.tester.tap_screen(129, 1010)
                self.action.tap(element).perform()

            # Recording authority
            element = self.tester.find_element_by_id("android:id/button1")
            if element is not None:
                self.tester.tap_screen(129, 1010)
                self.action.tap(element).perform()

            # Exit the viewfinder and return to the discovery page
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)
