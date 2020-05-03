#!usr/bin/python
# -*- coding:utf-8 -*-

from .BaseDevicePreProcess import *


class MEITUM4PreProcess(BaseDevicePreProcess):

    def __init__(self, tester):
        super(MEITUM4PreProcess, self).__init__(tester)

    def install_process(self):
        try:
            Log.logger.info("Device: %s launch app and handle GPS popup" % self.tester.device.device_name)

            while not self.driver.is_app_installed("com.nice.main"):
                time.sleep(2)

            self.driver.launch_app()

            time.sleep(7)

            # Get the coordinates of the allowed frame and click
            print('Delete the allow button and the program will continue to execute')
            self.driver.swipe(488, 710, 488, 710, 5)

        except Exception as e:
            Log.logger.info("Device: Error occurred in %s" % self.tester.device.device_name)
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def login_success_process(self):
        try:
            Log.logger.info(
                "Device: %s After successful login, process various automatic pop-up windows" % self.tester.device.device_name)

            time.sleep(4)
            print('Allow authorized address book permissions')
            self.driver.swipe(493, 705, 493, 705, 5)

        except Exception as e:
            Log.logger.info("Device: Error occurred in %s" % self.tester.device.device_name)
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def get_permission_process(self):
        Log.logger.info("Device: %s Get camera and recording permissions" % self.tester.device.device_name)
        try:
            # Open the framing frame
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            # Camera permissions
            time.sleep(2)
            print('Authorize camera permissions')
            self.driver.swipe(500, 721, 500, 721, 5)

            # Recording authority
            time.sleep(6)
            print('Authorized recording permission')
            self.driver.swipe(490, 722, 490, 722, 5)

            time.sleep(1)
            # Exit the viewfinder and return to the discovery page
            if self.tester.is_element_exist('com.nice.main:id/titlebar_return', 3):
                self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')
            else:
                self.tester.back_to_feed()
        except Exception as e:
            Log.logger.info("Device: Error occurred in %s" % self.tester.device.device_name)
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)
