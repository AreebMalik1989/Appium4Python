#!usr/bin/python
# -*- coding:utf-8 -*-

from .BaseDevicePreProcess import *


class OPPOR9PreProcess(BaseDevicePreProcess):

    def __init__(self, tester):
        super(OPPOR9PreProcess, self).__init__(tester)

    def install_process(self):
        Log.logger.info(
            "Device: %s handles various pop-up windows during installation" % self.tester.device.device_name)
        try:
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/btn_allow_once', 60)
        except TimeoutException as e:
            traceback.print_exc()
        finally:
            try:
                self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/bottom_button_two')
                self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/bottom_button_two')
                self.tester.find_element_by_id_and_tap('oppo:id/remember_cb')
                self.tester.find_element_by_id_and_tap('android:id/button1')
            except Exception as e:
                traceback.print_exc()
                DriverManager.quit_driver(self.tester.device.device_id)

    def login_success_process(self):
        Log.logger.info(
            "Device: %s After successful login, process various automatic pop-up windows" % self.tester.device.device_name)
        try:
            self.tester.find_element_by_id_and_tap('android:id/button1')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_cancel')
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
