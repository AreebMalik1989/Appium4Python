# coding=utf-8

from .BaseDevicePreProcess import *


class HTCD826wPreProcess(BaseDevicePreProcess):

    def __init__(self, tester):
        super(HTCD826wPreProcess, self).__init__(tester)

    def install_process(self):
        try:
            Log.logger.info("Device: %s launch app and handle installation" % self.tester.device.device_name)

            while not self.tester.is_element_exist('com.htc:id/primary'):
                time.sleep(1)

            time.sleep(2)
            self.tester.press_keycode(4)

            while not self.driver.is_app_installed("com.nice.main"):
                time.sleep(2)

            self.driver.launch_app()
        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def login_process(self):
        self.tester.find_element_by_id_and_tap('com.nice.main:id/login')
        self.tester.find_element_by_id_and_send_keys('com.nice.main:id/phone_number', self.user.mobile)
        self.tester.find_element_by_id_and_tap('com.nice.main:id/password')
        self.tester.find_element_by_id_and_send_keys('com.nice.main:id/password', self.user.password)
        self.tester.press_keycode(4)
        self.tester.find_element_by_id_and_tap('com.nice.main:id/login')

    def login_success_process(self):
        Log.logger.info("Device: %s After successful login, no need to deal with" % self.tester.device.device_name)

    def get_permission_process(self):
        Log.logger.info("Device: %s does not need to process" % self.tester.device.device_name)
