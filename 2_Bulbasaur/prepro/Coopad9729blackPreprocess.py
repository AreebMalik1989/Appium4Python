#!usr/bin/python
# -*- coding:utf-8 -*-

from .BaseDevicePreProcess import *


class Coopad9729blackPreprocess(BaseDevicePreProcess):

    def __init__(self, tester):
        super(Coopad9729blackPreprocess, self).__init__(tester)

    def install_process(self):
        try:
            Log.logger.info("Device: %s launch app and handle GPS popup" % self.tester.device.device_name)

            while not self.driver.is_app_installed("com.nice.main"):
                time.sleep(2)

            self.driver.launch_app()

            # Process to get the location popup
            self.tester.find_element_by_id_and_tap('com.yulong.android.seccenter:id/alertdlg_allowed')

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def login_success_process(self):
        try:
            Log.logger.info(
                "Device: %s After successful login, process various automatic pop-up windows" % self.tester.device.device_name)

            # Get contact permissions
            self.tester.find_element_by_id_and_tap('com.yulong.android.seccenter:id/alertdlg_allowed')

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def get_permission_process(self):
        Log.logger.info("Device: %s Get camera and recording permissions" % self.tester.device.device_name)
        try:
            # Open the framing frame
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            # Video permissions
            self.tester.find_element_by_id_and_tap('com.yulong.android.seccenter:id/alertdlg_allowed')
            # Recording permissions
            self.tester.find_element_by_id_and_tap('com.yulong.android.seccenter:id/alertdlg_allowed')

            self.tester.press_keycode(4)

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)
