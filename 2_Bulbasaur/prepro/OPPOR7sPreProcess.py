#!usr/bin/python
# -*- coding:utf-8 -*-

from .BaseDevicePreProcess import *


class OPPOR7sPreProcess(BaseDevicePreProcess):

    def __init__(self, tester):
        super(OPPOR7sPreProcess, self).__init__(tester)

    # Unable to obtain spatial information, click using coordinates
    def install_process(self):
        Log.logger.info(
            "Device: %s handles various pop-up windows during installation" % self.tester.device.device_name)

        try:
            while not self.driver.is_app_installed("com.nice.main"):
                time.sleep(2)
            self.driver.launch_app()
            # Click the pop-up window to no longer remind GPS permission
            self.tester.find_element_by_id_and_tap('oppo:id/remember_cb')
            time.sleep(2)
            # Click GPS to allow
            self.tester.find_element_by_id_and_tap('android:id/button1')
        except TimeoutException as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def login_success_process(self):
        Log.logger.info(
            "Device: %s After successful login, process various automatic pop-up windows" % self.tester.device.device_name)
        try:
            self.tester.find_element_by_id_and_tap('android:id/button1')
        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def get_permission_process(self):
        Log.logger.info("Device: %s Get camera and recording permissions" % self.tester.device.device_name)
        try:
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            # Camera permissions
            self.tester.find_element_by_id_and_tap('oppo:id/remember_cb')
            self.tester.find_element_by_id_and_tap('android:id/button1')

            # Recording permissions
            self.tester.find_element_by_id_and_tap('oppo:id/remember_cb')
            self.tester.find_element_by_id_and_tap('android:id/button1')

            # Close the viewfinder
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)
