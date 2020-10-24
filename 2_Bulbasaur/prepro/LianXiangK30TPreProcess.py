#!usr/bin/python
# -*- coding:utf-8 -*-

from .BaseDevicePreProcess import *


class LianXiangK30TPreProcess(BaseDevicePreProcess):

    def __init__(self, tester):
        super(LianXiangK30TPreProcess, self).__init__(tester)

    def install_process(self):
        try:
            Log.logger.info(
                "Device: %s handles various pop-up windows during installation" % self.tester.device.device_name)

            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().resourceId(\"com.lenovo.safecenter:id/btn_install\").textContains(\"确定\")')

            # Launch app
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

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def get_permission_process(self):
        Log.logger.info("Device: %s Get camera and recording permissions" % self.tester.device.device_name)
        try:
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            # Close the viewfinder
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)
