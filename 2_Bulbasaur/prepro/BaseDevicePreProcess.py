#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import threading

from common.DriverManager import *
from common.Log import *
from model.Tester import *


class BaseDevicePreProcess(object):

    def __init__(self, tester):
        self.tester = tester
        self.driver = self.tester.driver
        self.action = TouchAction(self.driver)
        self.user = self.tester.user

    # Start pretreatment process
    def pre_process(self):
        Log.logger.info("device：%s Start pretreatment process..." % self.tester.device.device_name)
        driver = self.tester.driver
        try:
            if driver.is_app_installed('com.nice.main'):
                Log.logger.info("device：%s Uninstall the old nice package" % self.tester.device.device_name)
                driver.remove_app('com.nice.main')
            Log.logger.info("device：%s Start installing the nice package for testing" % self.tester.device.device_name)
            thread = threading.Thread(target=self.install_process)
            thread.start()
            self.install_app()
            thread.join()
            Log.logger.info("device：%s Successful start" % self.tester.device.device_name)
            self.login_process()
            Log.logger.info("device：%s login successful" % self.tester.device.device_name)
            self.login_success_process()
            time.sleep(10)
            self.get_permission_process()
            time.sleep(3)
            self.tester.clean_mp4_file()  # Clear sd mp4 file during preprocessing
            Log.logger.info(
                "device：%s Successful preprocessing, start executing test cases" % self.tester.device.device_name)
        except Exception as e:
            Log.logger.info("device：%s Abnormal!" % self.tester.device.device_name)
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.device_id)
            return False
        return True

    # Installation process
    def install_app(self):
        self.driver.install_app(DataProvider.niceapk)

    # version upgrade
    def upgrade_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.device_id, DataProvider.nicelatestapk)
        subprocess.call(cmd, shell=True)

        time.sleep(5)
        self.driver.launch_app()

        self.tester.start_screen_record('Live gift opening')
        time.sleep(10)
        self.tester.stop_screen_record('Live gift opening')

    # The process includes handling various pop-up windows during installation and startup until you can click the login button
    def install_process(self):
        pass

    # The process includes clicking the login button to reach the login page and logging in
    def login_process(self):
        Log.logger.info(
            "device：%s Start logging in, use account:%s" % (self.tester.device.device_name, self.tester.user.mobile))
        try:
            # The login button of the new and old registration process uses the same resource_id, no special judgment is required for the login button

            # First get the login button object of the registration page
            register_login_element = self.tester.find_element_by_id('com.nice.main:id/login')

            # Click to Login
            self.action.tap(register_login_element).perform()

            time.sleep(2)

            login_phone_number_element = self.tester.find_element_by_id('com.nice.main:id/phone_number', 2)
            while login_phone_number_element is None:
                self.action.tap(register_login_element).perform()
                time.sleep(2)
                login_phone_number_element = self.tester.find_element_by_id('com.nice.main:id/phone_number', 2)

            # Enter account password
            login_phone_number_element.send_keys(self.user.mobile)
            login_password = self.tester.find_element_by_id('com.nice.main:id/password')
            self.action.tap(login_password).perform()
            login_password.send_keys(self.user.password)

            # Judge until the login is successful
            login_element = self.tester.find_element_by_id('com.nice.main:id/login')
            self.action.tap(login_element).perform()

            time.sleep(2)

            self.tester.screenshot("login successful")
        except Exception as e:
            raise

    # The process includes processing various automatic pop-up dialog boxes after successful login
    def login_success_process(self):
        pass

    # Handle all required permissions, such as: camera, recording
    def get_permission_process(self):
        pass

    def check_user_profile_pic(self):
        self.tester.find_element_by_id_and_tap('com.nice.main:id/btnTabProfile')
        self.tester.find_element_by_id_and_tap('com.nice.main:id/img_profile_avatar')
        time.sleep(3)
        if self.tester.is_element_exist('Edit_avatar'):
            print('This user did not add an avatar')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/img_publish_photo')
            time.sleep(3)
            if self.tester.is_element_exist('com.nice.main:id/image'):
                self.tester.find_element_by_uiautomator_and_tap(
                    'new UiSelector().resourceId(\"com.nice.main:id/image\").index(0)')
                self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_action_btn')
                self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_action_btn')
                time.sleep(5)  # Upload avatar to [me] page
            else:
                Log.logger.info('Upload avatar failed')
                self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')
                self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')
        else:
            print('This user has added an avatar')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/profile_black')

    # Create autotest folder and generate test pictures
    def data_prepare(self):
        Log.logger.info("device：%s Check file start" % self.tester.device.device_name)
        if self.tester.is_autotest_exit():
            time.sleep(1)
        else:
            Log.logger.info("device：%s Write test file" % self.tester.device.device_name)
            self.tester.pull_file_to_device()
            time.sleep(10)
            self.tester.refresh_test_pic()
