#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import traceback
import time
import threading

import common.DriverManager as DriverManager
import common.MonkeyResultWiki as MonkeyResultWiki
import common.MonkeyResultEmail as MonkeyResultEmail
import common.share as share

from appium import webdriver

from common.DeviceManager import *
from common.PreProManager import *
from common.TestCaseManager import *
from common.TheTestResult import *


class RunTestManager:

    def __init__(self, mode):
        self.count_test_cases = 0
        self.task_id = int(time.time())
        self.logger = Log.logger
        self.mode = mode

    def start_run(self):
        try:
            self.logger.debug('Start run %s...' % self.mode)
            if self.mode == "autotest":
                TheTestResult.create_result_folder()

            elif self.mode == "monkey":
                Tester.is_exit_monkeyresultfile()
                Tester.create_monkey_result()

            self.logger.info("Start task...")
            self.start_run_test()

            if self.mode == "autotest":
                self.logger.debug('Start generating test report...')
                TheTestResult.generate_html_test_result()

            elif self.mode == "monkey":
                # Read all the logs under this monkey result folder
                Tester.open_filelist()
                Tester.read_log()
                time.sleep(10)
                MonkeyResultWiki.login_and_post("parameter")
                MonkeyResultEmail.run()

            self.logger.info("Complete the test and exit all Drivers")
            # DriverManager.quit_all_driver()
            self.stop_run()
        except Exception as e:
            traceback.print_exc()
            self.stop_run()

    def stop_run(self):
        share.set_if_run(False)

    def run(self, tester):
        try:
            DataProvider.start_time[tester.device.device_id] = get_format_current_time()
            tester.show_relationship()
            # Start equipment pretreatment process
            if PreProManager(tester).device().pre_process():
                if self.mode == "monkey":
                    self.logger.info("device：%s ---Start monkey---" % tester.device.device_name)
                    suite = TestCaseManager(tester).monkey_android()
                    self.logger.info("device：%s ---monkey execution ends---" % tester.device.device_name)

                elif self.mode == "autotest":
                    tester.clean_mp4_file()  # Clean up mp4 files in DCIM folder of sd card
                    self.logger.info("device：%s ---Start auto tests---" % tester.device.device_name)
                    tester.pic_data_prepare()  # Determine if the phone has an auto test gallery
                    tester.video_data_prepare()  # Determine if the phone has auto_video video
                    self.logger.info("device：%s Start Load Test Case..." % tester.device.device_name)
                    suite = TestCaseManager(tester).compatibility_test_suite()
                    #suite = TestCaseManager(tester).signal_case_suit(test_show_pub_video)
                    self.logger.info("device：%s Test case Load completed" % tester.device.device_name)
                    self.logger.info("device：%s Start executing test cases..." % tester.device.device_name)
                    unittest.TextTestRunner(verbosity=2, resultclass=TheTestResult).run(suite)
                    self.logger.info("device：%s Test case execution completed" % tester.device.device_name)
            else:
                self.logger.info("device：%s Pre-processing process failed，Terminate the corresponding task" % tester.device.device_name)

            DataProvider.stop_time[tester.device.device_id] = get_format_current_time()

        except Exception as e:
            self.logger.info("device：%s Abnormal" % tester.device.device_name)
            traceback.print_exc()

    def init_tester_data(self, device, which_user):
        try:
            desired_caps = dict()
            desired_caps['platformName'] = device.platform_name
            desired_caps['platformVersion'] = device.platform_version
            desired_caps['deviceName'] = device.device_name
            desired_caps['unicodeKeyboard'] = "true"
            desired_caps['resetKeyboard'] = 'true'
            desired_caps['autoLaunch'] = "false"
            desired_caps['appPackage'] = 'com.nice.main'
            desired_caps['appActivity'] = 'com.nice.main.activities.MainActivity_'
            desired_caps['udid'] = device.device_id
            desired_caps['newCommandTimeout'] = "3000"
            desired_caps['unicodeKeyboard'] = True
            desired_caps['resetKeyboard'] = True
            url = "http://%s:%s/wd/hub" % (device.server, device.server_port)
            driver = webdriver.Remote(url, desired_caps)

            if self.mode=="autotest":
                # Create screenshot folders for each device
                folder_path = '%s/%s' % (TheTestResult.test_result_path, device.device_name)
                os.mkdir(folder_path)

            tester_object = Tester(driver)
            tester_object.device = device
            tester_object.user = DataProvider.users[which_user]
            tester_object.logger = self.logger
            if self.mode=="autotest":
                tester_object.screenshot_path = folder_path

            DriverManager.drivers[device.device_id] = driver
            return tester_object
        except Exception as e:
            self.logger.info("device：%s abnormal" % device.device_name)
            traceback.print_exc()

    def start_run_test(self):
        which_user = 0
        threads = []
        for deviceid, device in DeviceManager.server_devices.items():
            testerobject = self.init_tester_data(device, which_user)
            DataProvider.testers[device.device_id] = testerobject
            try:
                thread = threading.Thread(target=self.run, args=(testerobject,))
                thread.start()
                which_user = which_user + 1
                threads.append(thread)
            except Exception as e:
                traceback.print_exc()
                DataProvider.testers[deviceid].driver.quit()

        for thread in threads:
            thread.join()
