#!usr/bin/python
# -*- coding:utf-8 -*-

from .BaseDevicePreProcess import *


class HUAWEIVNSAL00PreProcess(BaseDevicePreProcess):

    def __init__(self, tester):
        super(HUAWEIVNSAL00PreProcess, self).__init__(tester)

    def install_process(self):
        try:
            Log.logger.info("Device: %s handles installation prompts" % self.tester.device.device_name)

            # self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/decide_to_continue')
            # self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/goinstall')

            while not self.driver.is_app_installed("com.nice.main"):
                time.sleep(2)

            self.driver.launch_app()

            # Installed apps list permissions
            self.tester.find_element_by_id_and_tap('com.huawei.systemmanager:id/btn_allow')

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def login_success_process(self):
        try:
            Log.logger.info(
                "Device: %s After successful login, process various automatic pop-up windows" % self.tester.device.device_name)

            # Access Request
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')
            time.sleep(1)
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_ok')
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

            Log.logger.info(
                "Device: %s has not successfully authorized the address book" % self.tester.device.device_name)

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def get_permission_process(self):
        Log.logger.info("Device: %s Get camera and recording permissions" % self.tester.device.device_name)
        try:
            # Open the framing frame
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')
            if self.tester.is_element_exist('com.huawei.systemmanager:id/btn_allow'):
                self.tester.tap_screen(730, 1170)
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')
            time.sleep(1)

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)
