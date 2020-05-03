#!usr/bin/python
# -*- coding:utf-8 -*-

from .BaseDevicePreProcess import *


class HuaWeiG9PreProcess(BaseDevicePreProcess):

    def __init__(self, tester):
        super(HuaWeiG9PreProcess, self).__init__(tester)

    def install_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.device_id, DataProvider.niceapk)
        subprocess.call(cmd, shell=True)

    # Start preprocessing process
    def pre_process(self):
        Log.logger.info("Device: %s starts preprocessing process ..." % self.tester.device.device_name)
        driver = self.tester.driver
        try:
            if driver.is_app_installed('com.nice.main'):
                Log.logger.info("device: %s uninstall the old nice package" % self.tester.device.device_name)
                driver.remove_app('com.nice.main')

            if self.tester.is_element_exist('android:id/button1', 30):
                self.tester.find_element_by_id_and_tap('android:id/button1')

            Log.logger.info(
                "device: %s started to install the nice package for testing" % self.tester.device.device_name)
            thread = threading.Thread(target=self.install_process)
            thread.start()
            self.install_app()
            thread.join()
            Log.logger.info("Device: %s started successfully" % self.tester.device.device_name)
            self.login_process()
            Log.logger.info("Device: %s successfully logged in" % self.tester.device.device_name)
            self.login_success_process()
            self.get_permission_process()
            time.sleep(3)
            self.tester.clean_mp4_file()  # clear sd mp4 file during preprocessing
            Log.logger.info(
                "Device: %s pre-processed successfully, start executing test cases" % self.tester.device.device_name)
        except  Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)
            return False
        return True

    def install_process(self):
        try:
            Log.logger.info("Device: %s launch app and handle GPS popup" % self.tester.device.device_name)

            if self.tester.is_element_exist('com.android.packageinstaller:id/decide_to_continue', 10):
                self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/decide_to_continue')
                self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/goinstall')
            elif self.tester.is_element_exist('com.android.packageinstaller:id/ok_button', 10):
                self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/ok_button')
            else:
                print('error!')
        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)
            # The process includes clicking the login button to reach the login page and log in
        finally:
            while not self.driver.is_app_installed("com.nice.main"):
                time.sleep(2)

            self.driver.launch_app()

            # Get positioning permission
            self.tester.find_element_by_id_and_tap('com.huawei.systemmanager:id/btn_allow')

    def login_process(self):
        Log.logger.info("device: %s to start logging in, using account:% s" % (
            self.tester.device.device_name, self.tester.user.mobile))
        try:
            # The login button of the new and old registration process uses the same resource_id, no special judgment
            # is required for the login button
            self.tester.find_element_by_id_and_tap('com.nice.main:id/login')
            self.tester.find_element_by_id_and_send_keys('com.nice.main:id/phone_number', self.user.mobile)
            self.tester.find_element_by_id_and_send_keys('com.nice.main:id/password', self.user.password)

            self.tester.press_keycode(4)

            time.sleep(1)
            self.tester.find_element_by_id_and_tap('com.nice.main:id/login')

            time.sleep(1)
            self.tester.screenshot("Login successful")
        except Exception as e:
            raise

    def login_success_process(self):
        try:
            Log.logger.info(
                "Device: %s After successful login, process various automatic pop-up windows" % self.tester.device.device_name)

            # Authorize sd card
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/do_not_ask_checkbox')
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

            # Authorized location information
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/do_not_ask_checkbox')
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

            # Authorized address book
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_ok')

            time.sleep(5)
            if self.tester.is_element_exist('com.android.packageinstaller:id/permission_allow_button'):
                self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/do_not_ask_checkbox')
                self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

            time.sleep(5)
            if self.tester.is_element_exist('com.nice.main:id/btn_know'):
                self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_know')

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)

    def get_permission_process(self):
        Log.logger.info("Device: %s Get camera and recording permissions" % self.tester.device.device_name)
        try:
            # Open the framing frame
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')

            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/do_not_ask_checkbox')
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/do_not_ask_checkbox')
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

            # Switch to shooting tab
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')
            time.sleep(1)

        except Exception as e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)
