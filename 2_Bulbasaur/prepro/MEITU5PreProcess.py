#!usr/bin/python
# -*- coding:utf-8 -*-

from .BaseDevicePreProcess import *


class MEITU5PreProcess(BaseDevicePreProcess):

    def __init__(self, tester):
        super(MEITU5PreProcess, self).__init__(tester)

    def install_process(self):
        try:
            Log.logger.info("Device: %s launch app and handle GPS popup" % self.tester.device.device_name)

            while not self.driver.is_app_installed("com.nice.main"):
                time.sleep(2)

            self.driver.launch_app()
        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def login_success_process(self):
        try:
            Log.logger.info(
                "Device: %s After successful login, process various automatic pop-up windows" % self.tester.device.device_name)

            # Permission management box
            # self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')
            # self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')
            # self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

            # Authorized address book box
            # self.tester.find_element_by_id_and_tap('com.nice.main:id/txt_time')

            # Address book permission application box
            self.tester.find_element_by_id_and_tap('com.mediatek.security:id/mts_button1')
        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def get_permission_process(self):
        Log.logger.info("Device: %s Get camera and recording permissions" % self.tester.device.device_name)
        try:
            # Open the framing frame
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            # Camera permissions
            self.tester.find_element_by_id_and_tap('com.mediatek.security:id/mts_button1')

            # Exit the viewfinder and return to the discovery page
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')
        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)
