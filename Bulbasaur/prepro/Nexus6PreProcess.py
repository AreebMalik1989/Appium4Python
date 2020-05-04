# coding=utf-8

from .BaseDevicePreProcess import *


class Nexus6PreProcess(BaseDevicePreProcess):

    def __init__(self, tester):
        super(Nexus6PreProcess, self).__init__(tester)

    def install_process(self):
        try:
            Log.logger.info("device: %s launch app" % self.tester.device.device_name)

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

            # The first login requires three authorizations: location information, access to photos and files,
            # making calls and managing calls
            for i in range(0, 3):
                self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')
                time.sleep(1)

            # nice authorized address book popup
            # self.tester.find_element_by_id_and_tap ('com.nice.main: id / btn_ok') #Cannot click on the control
            time.sleep(2)
            self.tester.tap_screen(700, 1660)

            # System authorization popup
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def get_permission_process(self):
        Log.logger.info("Device: %s Get camera and recording permissions" % self.tester.device.device_name)
        try:

            # self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')

            # Open the framing frame
            time.sleep(10)
            self.tester.tap_screen(745, 2300)

            # Permission to take photos and record videos
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

            # Record audio permission
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

            # Switch to the shooting page
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            # Exit the viewfinder and return to the discovery page
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')

            time.sleep(10)
            if self.tester.is_element_exist('You follow people\'s stories and live streaming '):
                # Handling language issues
                self.tester.find_element_by_id_and_tap('com.nice.main:id/btnTabProfile')
                while not self.tester.is_element_exist('com.nice.main:id/layout_profile_setting'):
                    self.tester.swipe_down()
                self.tester.find_element_by_id_and_tap('com.nice.main:id/layout_profile_setting')
                self.tester.find_element_by_id_and_tap('com.nice.main:id/layout_setting_common')
                self.tester.find_element_by_id_and_tap('com.nice.main:id/layout_setting_language')
                time.sleep(3)

                # Simplified Chinese language
                if self.tester.is_element_exist(u'Simplified Chinese '):
                    self.tester.back_to_feed()
                else:
                    self.tester.find_element_by_id_and_tap('com.nice.main:id/layout_setting_language')
                    time.sleep(2)
                    self.tester.find_element_by_xpath_and_tap('//android.widget.TextView[2]')
                    self.tester.back_to_feed()
            else:
                print('nexus6 is currently simplified Chinese')

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)
