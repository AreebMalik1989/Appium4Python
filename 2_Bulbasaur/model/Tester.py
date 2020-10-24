#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import functools
import math
import operator
import random
import shutil
import subprocess
import tempfile
import time
import traceback

from PIL import Image
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common.DataProvider import DataProvider
from common.PublicMethod import *

PATH = lambda p: os.path.abspath(p)
TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")


class Tester(object):

    def __init__(self, driver):
        self._driver = driver
        self._user = None
        self._device = None
        self._logger = None
        self.action = TouchAction(self._driver)
        self._screenshot_path = ""
        self.device_width = self._driver.get_window_size()['width']
        self.device_height = self._driver.get_window_size()['height']

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, value):
        self._driver = value

    @property
    def screenshot_path(self):
        return self._screenshot_path

    @screenshot_path.setter
    def screenshot_path(self, value):
        self._screenshot_path = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, value):
        self._device = value

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value

    def show_relationship(self):
        self.logger.info("Correspondence between equipment and login number %s ----- %s" % (self.device.device_name, self.user.mobile))

    def swipe_screen(self, startx, starty, endx, endy, duration=500):
        self.logger.info("device：%s swipe from point x:%s y:%s to x:%s y:%s"
                         % (self.device.device_name, startx, starty, endx, endy))
        self.driver.swipe(startx, starty, endx, endy, duration=500)

    def tap_screen(self, x, y):
        self.logger.info("device：%s tap screen point at x:%s y:%s" % (self.device.device_name, x, y))
        self.action.tap(None, x, y).perform()

    def get_screen_center(self):
        x = self.device_width / 2
        y = self.device_height / 2

        y1 = 10

        self.swipe_screen(x, y, x, y1)

    def tap_screen_center(self):
        x = self.device_width / 2
        y = self.device_height / 2
        self.logger.info("device：%s tap center of the screen point at x:%s y:%s" % (self.device.device_name, x, y))
        self.action.tap(None, x, y).perform()

    def long_press_screen(self, eleid, duration):
        el = self.driver.find_element_by_id(eleid)
        time.sleep(1)
        self.logger.info("device：%s Long press the control %s %s millisecond" % (self.device.device_name, eleid, duration))
        self.action.long_press(el).wait(duration).release().perform()

    def screenshot(self, name):
        path = "%s/%s.png" % (self.screenshot_path, name)
        self.driver.save_screenshot(path)
        self.logger.info("device：%s screen shot at path:%s" % (self.device.device_name, path))

    def screenshot2(self, name):
        path = "%s/%s.jpg" % (self.screenshot_path, name)
        self.driver.save_screenshot(path)
        self.logger.info("device：%s screen shot at path:%s" % (self.device.device_name, path))

    def start_screen_record(self, name):
        """ Start recording screen operation
            After the operation is completed, the stop_screen_record () method is executed
            The system defaults to a maximum of 180 seconds, please complete all operations within 180 seconds

        :Args:
         - name - The name of the file to be saved, supports Chinese
        :Usage:
            self.tester.start_screen_record('Recorded video test')
        """
        start_record = "adb -s %s shell screenrecord /sdcard/DCIM/%s.mp4" % (self.device.device_id, name)
        self.logger.info("device：%s screen record started" % self.device.device_name)
        subprocess.Popen(start_record, shell=True)

    def stop_screen_record(self, name):
        """ End recording screen operation
            note！！！！！
            The name value of the parameter must be the same as the name value in strat_screen_record ()

        :Args:
         - name - Same as the name passed in start_screen_record ()
        :Usage:
            self.tester.start_screen_record('Recorded video test')
            Your code here
            self.tester.stop_screen_record(u'Recorded video test')
        """
        self.logger.info("device：%s screen record is stopping" % self.device.device_name)
        keyword = 'screenrecord'
        cmd_pid = "ps -e| grep adb |awk '{if($6=/%s/ && $8=/%s/)print $1}'" % (self.device.device_id, keyword)
        pid = os.popen(cmd_pid).read()
        kill_pid = "kill -9 %s" % pid
        subprocess.Popen(kill_pid, shell=True)
        time.sleep(3)
        cmd_file = "adb -s %s shell ls /sdcard/DCIM/ |grep %s" % (self.device.device_id, name)
        name = os.popen(cmd_file).read().strip('\r\n')
        path = "%s/%s" % (self.screenshot_path, name)
        cmd_pull = "adb -s %s pull /sdcard/DCIM/%s %s" % (self.device.device_id, name, self.screenshot_path)
        subprocess.Popen(cmd_pull, shell=True)

    def clean_mp4_file(self):
        clean_cmd = "adb -s %s shell rm /sdcard/DCIM/*.mp4" % self.device.device_id
        self.logger.info("device：%s Clean up mp4 files recorded by sd card" % self.device.device_name)
        subprocess.Popen(clean_cmd, shell=True)

        print('clean done')

    def find_element_by_id(self, eleid, timeout=120):
        self.logger.info("device：%s start find :%s" % (self.device.device_name, eleid))
        try:
            element = self.wait_element_id_display(self.driver, eleid, eleid, timeout)
            return element
        except Exception as e:
            self.logger.info("device：%s Abnormal!" % self.device.device_name)
            traceback.print_exc()
            return None

    def find_element_by_id_and_tap(self, eleid, timeout=120, taptimes=1):
        self.logger.info("device：%s start tap :%s" % (self.device.device_name, eleid))
        try:
            element = self.wait_element_id_display(self.driver, eleid, eleid, timeout)
            if element is not None:
                if taptimes == 1:
                    self.action.tap(element).perform()
                    self.logger.info("device：%s tap success :%s " % (self.device.device_name, eleid))
                elif taptimes > 1:
                    for x in range(taptimes):
                        self.action.tap(element).perform()
                        self.logger.info("device：%s tap success :%s " % (self.device.device_name, eleid))
        except TimeoutException as e:
            self.logger.info("device：%s Abnormal!" % self.device.device_name)
            traceback.print_exc()

    def find_element_by_uiautomator(self, uiselector, timeout=200):
        self.logger.info("device：%s start find element uiselector:%s" % (self.device.device_name, uiselector))
        element = self.wait_element_uiautormator_display(self.driver, uiselector, uiselector, timeout)
        return element

    def find_element_by_uiautomator_and_tap(self, uiselector, timeout=200):
        self.logger.info("device：%s start tap element uiselector:%s" % (self.device.device_name, uiselector))
        element = self.wait_element_uiautormator_display(self.driver, uiselector, uiselector, timeout)
        if element is not None:
            self.action.tap(element).perform()
            self.logger.info("device：%s tap success :%s " % (self.device.device_name, uiselector))

    def find_element_by_id_and_send_keys(self, eleid, text, timeout=200):
        self.logger.info("device：%s start send_key %s to element id:%s" % (self.device.device_name, text, eleid))
        element = self.wait_element_id_display(self.driver, eleid, eleid, timeout)
        if element is not None:
            element.send_keys(text)
            self.logger.info("device：%s send_key text:%s to element id:%s success "
                             % (self.device.device_name, text, eleid))

    def find_element_by_class_name_and_tap(self, class_name, timeout=200):
        self.logger.info("device：%s start tap element class name:%s" % (self.device.device_name, class_name))
        element = self.wait_element_id_display(self.driver, class_name, class_name, timeout)
        if element is not None:
            self.action.tap(element).perform()
            self.logger.info("device：%s tap element id:%s success" % (self.device.device_name, class_name))

    def wait_element_id_display(self, driver, idstr, msg, timeout=200):
        try:
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, idstr)), msg)
        except TimeoutException as e:
            raise

    def wait_element_uiautormator_display(self, driver, uiselector, msg, timeout=200):
        try:
            return WebDriverWait(driver, timeout).until(lambda dr: dr.find_element_by_android_uiautomator(uiselector))
        except TimeoutException as e:
            raise

    def find_element_by_xpath_and_tap(self, xpath):
        self.logger.info("device：%s find by xpath:%s" % (self.device.device_name, xpath))
        element = self.driver.find_element_by_xpath(xpath)
        self.action.tap(element).perform()

    def wait_element(self, eleid, timeout=200):
        self.logger.info("device：%s wait element: %s" % (self.device.device_name, eleid))
        if self.wait_element_id_display(self.driver, eleid, eleid, timeout):
            self.logger.info("device：%s element id have displayed:%s" % (self.device.device_name, eleid))
        else:
            self.logger.info("device：%s Timeout: wait element %s" % (self.device.device_name, eleid))

    def press_keycode(self, keycode, metastate=None):
        """ Send the keycode to the device. Android devices only
            More about keycode please refer to
            http://developer.android.com/reference/android/view/KeyEvent.html.

        :Args:
         - keycode - The keycode value to be sent
         - metastate - meta information about the keycode being sent
        :Usage:
            self.tester.press_keycode(24)
        """
        self.logger.info("device：%s [action]Press the system button(keycode='%s')"
                         % (self.device.device_name, keycode))
        self.driver.press_keycode(keycode)

    # At present, the keycode button of the system is only 500ms long, which does not meet the needs for the time being.
    def long_press_keycode(self, keycode, metastate=None):
        """ Send the long press keycode event to the device. Android devices only
            Android only.

        :Args:
         - keycode - The keycode value to be sent
         - metastate - meta information about the keycode being sent
        :Usage:
            self.tester.long_press_keycode(24)
        """
        self.logger.info("device：%s [action]Long press the system button(keycode='%s')"
                         % (self.device.device_name, keycode))
        self.driver.long_press_keycode(keycode)

    def swipe_left(self, duration=None):
        """Perform a swipe left full screen width

        :Args:
            - None
        :Usage:
            self.tester.swipe_left()
        """
        self.logger.info("device：%s [action]Swipe left" % self.device.device_name)
        startx = self.device_width - 10
        starty = self.device_height / 2
        endx = 10
        endy = self.device_height / 2
        self.driver.swipe(startx, starty, endx, endy)

    def fast_swipe_left(self):
        """ Fast swipe left
        :Args:
            - None
        :Usage:
            self.tester.fast_swipe_left()
        """
        self.logger.info("device：%s [action]Swipe left" % self.device.device_name)
        startx = self.device_width - 10
        starty = self.device_height / 2
        endx = 10
        endy = self.device_height / 2
        self.driver.swipe(startx, starty, endx, endy, duration=200)

    def swipe_right(self, duration=None):
        """ Perform a swipe right full screen width

        :Args:
            - None
        :Usage:
            self.tester.swipe_right()
        """
        self.logger.info("device：%s [action]Swipe right " % self.device.device_name)
        startx = 10
        starty = self.device_height / 2
        endx = self.device_width - 10
        endy = self.device_height / 2
        self.driver.swipe(startx, starty, endx, endy)

    def fast_swipe_right(self):
        """ Swipe right
        :Args:
            - None
        :Usage:
            self.tester.fast_swipe_right()
        """
        self.logger.info("device：%s [action]Swipe right " % self.device.device_name)
        startx = 10
        starty = self.device_height / 2
        endx = self.device_width - 10
        endy = self.device_height / 2
        self.driver.swipe(startx, starty, endx, endy, duration=200)
        time.sleep(2)

    def swipe_down(self, duration=None):
        """Perform a swipe down full screen width
        :Args:
            - None
        :Usage:
            self.tester.swipe_down()
        """
        self.logger.info("device：%s [action]Swipe up " % self.device.device_name)
        startx = self.device_width / 2
        starty = self.device_height / 3
        endx = self.device_width / 2
        endy = 10
        self.driver.swipe(startx, starty, endx, endy)
        time.sleep(2)

    def swipe_down_refresh(self):
        startx = self.device_width / 2
        starty = self.device_height / 3
        endx = self.device_width / 2
        endy = self.device_height
        self.driver.swipe(startx, starty, endx, endy)
        time.sleep(2)

    def fast_swipe_down(self):
        """ Fast swipe down
        :Args:
            - None
        :Usage:
            self.tester.fast_swipe_down()
        """
        self.logger.info("device：%s [action]Swipe down " % self.device.device_name)
        startx = self.device_width / 2
        starty = self.device_height / 2
        endx = startx
        endy = starty - 300
        self.driver.swipe(startx, starty, endx, endy, duration=150)

    def fast_swipe_up(self):
        """ Slide up
        :Args:
            - None
        :Usage:
            self.tester.swipe_down()
        """
        self.logger.info("device：%s [action]Swipe down " % self.device.device_name)
        startx = self.device_width / 2
        starty = self.device_height / 2
        endx = startx
        endy = starty + 300
        self.driver.swipe(startx, starty, endx, endy, duration=150)

    def random_swipe_horizontal(self):
        direction = self.random_choice(("right", "left"))
        if direction == "right":
            self.fast_swipe_left()
        else:
            self.fast_swipe_right()

    def pull_to_refresh_page(self, duration=None):
        """ Pull down to refresh the page, disabled when the current page is not at the top
        :Args:
            - None
        :Usage:
            self.tester.pull_to_refresh_page()
        """
        self.logger.info("device：%s [action]Pull down to refresh the page  " % self.device.device_name)
        startx = self.device_width / 2
        starty = self.device_height / 3
        endx = self.device_width / 2
        endy = self.device_height - 10
        self.driver.swipe(startx, starty, endx, endy, duration=100)
        time.sleep(2)

    def pull_to_refresh_page2(self, duration=None):
        # The dragging distance is larger, the live card page will slide up, so as not to affect other pages, write a new one
        self.logger.info("device：%s [action]Drop down to refresh live card  " % self.device.device_name)
        startx = self.device_width / 2
        starty = self.device_height / 7
        endx = self.device_width / 2
        endy = self.device_height / 3
        self.driver.swipe(startx, starty, endx, endy, duration=10000)
        time.sleep(2)

    def is_element_exist(self, element, timeout=1):
        """ Determine if the element exists, return True if it exists, No if it doesn't exist
            Increase timeout timeout wait, the default is 1 time, can be overwritten by the parameters passed

        :Args:
            - element - Element to find
        :Usage:
            self.tester.is_element_exist('com.nice.main:id/beauty_auto')  # Beauty button
        """
        # self.logger.info("device：%s Find controls %s" % (self.device.devicename, element))
        count = 0
        while count < timeout:
            source = self.driver.page_source
            if element in source:
                # self.logger.info("device：%s Find the control: %s" % (self.device.devicename, element))
                return True
            else:
                count += 1
                time.sleep(1)
        # self.logger.info("device：%s Control not found: %s" % (self.device.devicename, element))
        return False

    def get_center_coor_and_tap(self, element):
        x = element.location['x']
        y = element.location['y']
        width = element.size['width']
        height = element.size['height']
        x = x + width / 2
        y = y + height / 2
        time.sleep(1)
        self.tap_screen(x, y)

    def get_center_loction(self, element):
        x = element.location['x']
        y = element.location['y']
        width = element.size['width']
        height = element.size['height']
        x = x + width / 2
        y = y + height / 2
        return x, y

    def is_autotest_exit(self):
        """ When initially talking to the device, determine whether there is an autotest test picture
        :Usage:
            self.pull_file_to_device  # Beauty button
        """
        cmd = "adb -s %s shell ls /sdcard/DCIM/ | grep autotest" % self.device.device_id
        result = "autotest"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if output.strip('\r\n') == result:
            self.logger.info("device：%s There are test pictures in SD " % self.device.device_id)
            return True
        else:
            self.logger.info("device：%s There is no test picture in SD " % self.device.device_id)
            return False

    def is_auto_video_exit(self):
        """ When initially talking to the device, determine whether there is an autotest test picture
        :Usage:
            self.pull_file_to_device  # Beauty button
        """
        cmd = "adb -s %s shell ls /sdcard/DCIM/ | grep auto_video" % self.device.device_id
        result = "auto_video"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if output.strip('\r\n') == result:
            self.logger.info("device：%s Test video exists in SD " % self.device.device_id)
            return True
        else:
            self.logger.info("device：%s There is no test video in SD " % self.device.device_id)
            return False

    def random_choice(self, string):
        return random.choice(string)

    # Determine if there is an autotest gallery locally on the phone
    def pic_data_prepare(self):
        # Log.logger.info("device：%s Check file start" % self.tester.device.devicename)
        if self.is_autotest_exit():
            time.sleep(1)
        else:
            # Log.logger.info("device：%s Write test file" % self.tester.device.devicename)
            self.pull_pic_file_to_device()
            time.sleep(10)
            self.refresh_test_pic()

    # Determine if there is auto_video video locally
    def video_data_prepare(self):
        # Log.logger.info("device：%s Check file start" % self.tester.device.devicename)
        if self.is_auto_video_exit():
            time.sleep(1)
        else:
            # Log.logger.info("device：%s Write test file" % self.tester.device.devicename)
            self.pull_video_file_to_device()
            time.sleep(10)
            self.refresh_test_video()

    def pull_pic_file_to_device(self):
        """ When initially talking to the device, copy the picture into the device
        :Usage:
            self.pull_pic_file_to_device
        """
        path = os.getcwd() + '/res/autotest'
        cmd = "adb -s %s push %s /sdcard/DCIM/" % (self.device.device_id, path)
        subprocess.Popen(cmd, shell=True)
        time.sleep(5)

    def pull_video_file_to_device(self):
        """ When initially talking to the device, copy the short video into the device
        :Usage:
            self.pull_file_to_device  video_
        """
        path = os.getcwd() + '/res/auto_video'
        cmd = "adb -s %s push %s /sdcard/DCIM/" % (self.device.device_id, path)
        subprocess.Popen(cmd, shell=True)
        time.sleep(5)

    def refresh_test_pic(self):
        """ When initializing the device, refresh the system gallery to make the autotest file visible
        :Usage:
            self.tester.refresh_test_pic()
        """
        img_src = os.getcwd() + '/res/autotest'
        path = get_file_name_from_path(img_src, 'jpg')
        for i in range(len(path)):
            cmd = "adb -s %s shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///storage/emulated/0/DCIM/autotest/%s.jpg" % (
                self.device.device_id, path[i])
            subprocess.Popen(cmd, shell=True)
            i += 1

    def refresh_test_video(self):
        """ When initializing the device, refresh the system gallery to make the auto_video file visible
        :Usage:
            self.tester.refresh_test_pic()
        """
        img_src = os.getcwd() + '/res/auto_video'
        path = get_file_name_from_path(img_src, 'mp4')
        for i in range(len(path)):
            cmd = "adb -s %s shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///storage/emulated/0/DCIM/auto_video/%s.mp4" % (
                self.device.device_id, path[i])
            subprocess.Popen(cmd, shell=True)
            i += 1

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Common processing methods~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def back_to_feed(self):
        """ Return to the feed homepage after the user case ends
        :Usage:
            self.tester.back_to_feed()
        """
        if self.is_element_exist('com.nice.main:id/btnTabSubscription'):
            time.sleep(1)
        else:
            self.driver.close_app()
            self.logger.info("device：%s close app " % self.device.device_name)
            time.sleep(5)
            self.driver.launch_app()
            self.logger.info("device：%s restart app " % self.device.device_name)
            time.sleep(10)

    def clear_pub_story(self):
        """ Delete the published story to prevent verification that affects other cases
        :Usage:
            self.tester.clear_pub_story()
        """
        if not self.is_element_exist('com.nice.main:id/btnTabSubscription', timeout=20):
            self.back_to_feed()

        # Enter my story
        if self.is_element_exist('my_story'):
            self.find_element_by_xpath_and_tap(
                '//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[2]')
        else:
            self.logger.info("device：%s My story does not exist " % self.device.device_name)

        # Delete published stories
        while self.is_element_exist('upload failed'):
            try:
                self.driver.find_element_by_id('com.nice.main:id/img_share').click()
                self.driver.find_element_by_android_uiautomator('text("Abandon upload")').click()
            except:
                self.logger.info("device：%s No click to story menu " % self.device.device_name)

        while self.is_element_exist('com.nice.main:id/more_share'):
            try:
                self.driver.find_element_by_id('com.nice.main:id/more_share').click()
                self.driver.find_element_by_android_uiautomator('text("delete")').click()
                self.driver.find_element_by_id('com.nice.main:id/btn_ok').click()
            except:
                self.logger.info("device：%s No click to story menu " % self.device.device_name)

    def get_verify_code(self):
        """ Get SMS verification code of current mobile phone number
        :Usage:
            self.tester.get_verify_code()
        """
        getverifycode = os.getcwd() + '/getverifycode.sh'
        sinput = "sh %s %s" % (getverifycode, self.user.mobile)
        myproc = subprocess.Popen(sinput, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        strout = myproc.stdout.read().decode("utf-8")
        code = strout.strip()
        self.logger.info("device：%s The login verification code is: %s " % (self.device.device_name, code))
        if not code:
            print("get vertifycode failed！！！")
        return code

    def longin_with_verifycode(self):
        """ Handle the SMS verification code link in the login process
        :Usage:
            self.tester.longin_with_verifycode()
        """
        if self.is_element_exist('com.nice.main:id/btn_phone_verify', timeout=5):
            self.logger.info("device：%s SMS verification is required to log in" % self.device.device_name)
            self.find_element_by_id_and_tap('com.nice.main:id/btn_phone_verify')
            time.sleep(2)
            code = self.get_verify_code()
            self.find_element_by_id_and_send_keys('com.nice.main:id/verification_code', code)
            time.sleep(2)
            if self.is_element_exist('com.nice.main:id/titlebar_action_btn'):
                self.find_element_by_id_and_tap('com.nice.main:id/titlebar_action_btn')
        else:
            self.logger.info("device：%s No SMS verification to log in" % self.device.device_name)

    # Take a picture of the specified area and store it in the specified folder
    def get_screen_shot_target_size(self, start_x, start_y, end_x, end_y, dir_path, image_name, form='png'):
        # Custom interception range
        # First capture the entire screen and store it in the system temporary directory
        self.driver.get_screenshot_as_file(TEMP_FILE)
        box = (start_x, start_y, end_x, end_y)
        image = Image.open(TEMP_FILE)
        new_image = image.crop(box)
        new_image.save(TEMP_FILE)

        # Copy the screenshot file to the specified directory
        # dirPath Before calling the method, you need to define the storage location of the picture yourself.
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        shutil.copyfile(TEMP_FILE, PATH(dir_path + "/" + image_name + "." + form))

        print('Screenshot succeeded')

    # Intercept picture similarity comparison by specifying elements
    def get_screen_element_and_compare(self, eleid, image_path, percent=0):
        # When using this method, you need to define the image_path first, that is, define the absolute path to store the target image
        # The target image is stored in the res / image_compare folder
        # percent is the similarity, the default is 0, which means that the similarity is 100% v

        # First capture the entire screen and store it in the system temporary directory
        self.driver.get_screenshot_as_file(TEMP_FILE)
        # Get the area occupied by the element
        location = eleid.location
        size = eleid.size
        box = (location["x"], location["y"], location["x"] + size["width"], location["y"] + size["height"])
        # Intercept the picture corresponding to the element
        image = Image.open(TEMP_FILE)
        new_image = image.crop(box)
        new_image.save(TEMP_FILE)

        # Load target image for comparison
        if os.path.isfile(image_path):
            load = Image.open(image_path)
        else:
            raise Exception("%s is not exist" % image_path)

        # Compare screenshots and local pictures
        histogram1 = Image.open(TEMP_FILE).histogram()
        histogram2 = load.histogram()

        differ = math.sqrt(functools.reduce(operator.add, list(map(lambda a, b: (a - b) ** 2,
                                                                   histogram1, histogram2))) / len(histogram1))
        if differ <= percent:
            print('Similarity matches the set percentage')
            return True
        else:
            print('Similarity does not match the set percentage')
            return False

    # Intercept picture similarity comparison by specifying size area
    def get_screen_target_size_and_compare(self, start_x, start_y, end_x, end_y, image_path, percent=0):
        # When using this method, you need to define the image_path first, that is, define the absolute path to store the target image
        # The target image is stored in the res / image_compare folder
        # percent is the similarity, the default is 0, which means the similarity is 100%

        # Custom interception range
        self.driver.get_screenshot_as_file(TEMP_FILE)
        box = (start_x, start_y, end_x, end_y)
        image = Image.open(TEMP_FILE)
        new_image = image.crop(box)
        new_image.save(TEMP_FILE)

        # Load target image for comparison
        if os.path.isfile(image_path):
            load = Image.open(image_path)
        else:
            raise Exception("%s is not exist" % image_path)

        # Compare screenshots and local pictures
        histogram1 = Image.open(TEMP_FILE).histogram()
        histogram2 = load.histogram()

        differ = math.sqrt(functools.reduce(operator.add, list(map(lambda a, b: (a - b) ** 2,
                                                                   histogram1, histogram2))) / len(histogram1))
        if differ <= percent:
            print('Similarity matches the set percentage')
            return True
        else:
            print('Similarity does not match the set percentage')
            return False

    def input_int(self, strings):
        # print("Parameters passed" + str(strings))
        my_dict = {'0': '7', '1': '8', '2': '9', '3': '10', '4': '11',
                   '5': '12', '6': '13', '7': '14', '8': '15', '9': '16'}
        for i in range(len(strings)):
            i = strings[i]
            # print('The value in the string' + str(i))
            keywords = my_dict[i]
            # print('String converted value' + str(keywords))
            self.driver.press_keycode(keywords)

    def set_input_method(self):
        true_value = "com.google.android.inputmethod.pinyin/.PinyinIME"
        package_name = "com.google.android.inputmethod.pinyin"
        command0 = 'adb -s %s shell ime list -s | grep %s' % (self.device.device_id, true_value)
        command1 = 'adb -s %s shell settings get secure default_input_method | grep %s' % (
            self.device.device_id, true_value)
        command2 = 'adb -s %s shell ime set %s' % (self.device.device_id, true_value)
        install_akp = "adb -s %s install -r %s" % (self.device.device_id, DataProvider.inputmethod)
        p = os.popen(command0)
        outstr = p.read()
        if outstr != true_value:
            subprocess.call(install_akp, shell=True)
        p1 = os.popen(command1)
        outstr = p1.read()
        if outstr != true_value:
            subprocess.call(command2, shell=True)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Common case steps~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def pub_nice_pic(self):

        self.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
        self.is_element_exist("nice")

        # Click on the album to select
        self.find_element_by_id_and_tap('com.nice.main:id/titlebar_center_title')

        # Switch to autotest album
        time.sleep(3)
        while not self.is_element_exist('autotest'):
            self.swipe_down()
            time.sleep(1)

        self.find_element_by_uiautomator_and_tap(
            'new UiSelector().resourceId(\"com.nice.main:id/txt_name\").textContains(\"autotest\")')

        # Choose 9 pictures
        time.sleep(3)
        for i in range(9):
            time.sleep(2)
            self.find_element_by_uiautomator_and_tap(
                'new UiSelector().resourceId(\"com.nice.main:id/select_textview_container\").index(1)')

        # Click Next to reach the editing page
        time.sleep(3)
        self.find_element_by_id_and_tap('com.nice.main:id/titlebar_next')

        # Get the center coordinates of the image Container and click to pop up the tab page
        time.sleep(10)
        if self.is_element_exist('com.nice.main:id/btn_panel_crop'):
            time.sleep(2)
            self.tap_screen_center()

        # Add tag autotest
        time.sleep(1)
        self.find_element_by_id_and_send_keys('com.nice.main:id/txt_search', 'autotest')
        self.find_element_by_uiautomator_and_tap(
            'new UiSelector().resourceId(\"com.nice.main:id/tv_tag_name\").index(0)')

        # Click Next to reach the preview page
        self.find_element_by_id_and_tap('com.nice.main:id/title_next_btn')

        # Add to
        self.find_element_by_id_and_send_keys('com.nice.main:id/publish_content_text', '123456')

        # Click the publish button
        self.find_element_by_id_and_tap('com.nice.main:id/titlebar_next_btn')
        time.sleep(10)
        self.back_to_feed()
        print("pub_nine_pic finished")

    def find_pub_nice_pic(self):
        text = "123456"
        for i in range(20):
            if self.is_element_exist(text):
                self.driver.find_element_by_android_uiautomator('text("123456")')
                self.logger.info("device: %s Find the post mark: %s " % (self.device.device_name, text))
                return True
            else:
                self.swipe_down()
                i += 1
        self.logger.info("device: %s No post mark found: %s " % (self.device.device_name, text))
        return False

    def enter_my_profile(self):
        self.back_to_feed()
        self.find_element_by_id_and_tap('com.nice.main:id/btnTabProfile')
        self.find_element_by_id_and_tap('com.nice.main:id/layout_profile_base_container')
        if self.is_element_exist("com.nice.main:id/profile_edit", timeout=10):
            self.logger.info("device: %s Successfully entered the personal page" % self.device.device_name)
        else:
            self.logger.info("device: %s Failed to enter personal page" % self.device.device_name)

    def enter_live_from_disc_page(self):
        self.back_to_feed()
        self.driver.find_element_by_id('com.nice.main:id/btnTabExplore').click()
        if self.is_element_exist('com.nice.main:id/recommend_live_rv', timeout=10):
            time.sleep(5)
            self.find_element_by_xpath_and_tap('//android.widget.RelativeLayout[3]')
        else:
            self.find_element_by_id_and_tap('com.nice.main:id/bg_live_card')
        time.sleep(5)
        self.find_element_by_id_and_tap('com.nice.main:id/img_pic')
        if self.is_element_exist('com.nice.main:id/btn_exit', timeout=5):
            return True
        elif self.is_element_exist('com.nice.main:id/exit_btn', timeout=5):
            return True
        else:
            return False

    def calculate_element_center_and_tap(self, element):
        self.ele = self.driver.find_element_by_id(element)
        x = self.ele.location['x']
        y = self.ele.location['y']
        width = self.ele.size['width']
        height = self.ele.size['height']
        x1 = x + width / 2
        y1 = y + height / 2
        time.sleep(1)
        self.tap_screen(x1, y1)

    def enter_hot_live_list(self):
        self.back_to_feed()
        self.driver.find_element_by_id('com.nice.main:id/btnTabExplore').click()
        if self.is_element_exist('com.nice.main:id/recommend_live_rv', timeout=10):
            time.sleep(5)
            self.find_element_by_xpath_and_tap('//android.widget.RelativeLayout[3]')
        else:
            self.find_element_by_id_and_tap('com.nice.main:id/bg_live_card')
        time.sleep(5)

    def find_mutil_pic_profile(self):
        if self.is_element_exist('9'):
            return True
        else:
            for i in range(20):
                self.swipe_down()
                if self.is_element_exist('9'):
                    self.logger.info("device: %s 9 pictures found" % self.device.device_name)
                    return True
                else:
                    i += 1
            self.logger.info("device: %s 9 pictures found" % self.device.device_name)
            return False

    def exit_from_watch_live(self):
        """
        Exit from watching live
        """
        if self.is_element_exist('com.nice.main:id/btn_exit', timeout=5):
            self.find_element_by_id_and_tap('com.nice.main:id/btn_exit')
            if self.is_element_exist('com.nice.main:id/btn_exit'):
                self.find_element_by_id_and_tap('com.nice.main:id/btn_exit')
        else:
            self.find_element_by_id_and_tap('com.nice.main:id/exit_btn')

    def enter_story_pub_page(self):
        """ Enter the story shooting page from the feed page, and handle the logic such as guidance and prompting
        :Usage:
            self.tester.clear_pub_story()
        """
        # Confirm on the feed homepage
        self.back_to_feed()

        # Feed page slide to open story shooting page
        self.swipe_right()

        # Handle the guide or pop-up window when entering the story for the first time
        if self.is_element_exist('Your phone does not support the story feature'):
            self.logger.info("device：%s Does not support story function " % self.device.device_name)
            self.screenshot("Does_not_support_story_function")
            self.find_element_by_id_and_tap('com.nice.main:id/btn_ok')
            self.back_to_feed()
            return False
        else:
            time.sleep(2)
            self.tap_screen_center()
            return True

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ end common case steps~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ monkey~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Define a class variable to create the monkey result folder
    monkey_result_path = ""
    monkey_log = os.getcwd() + '/Monkey_log'

    @classmethod
    def is_exit_monkeyresultfile(cls):
        if os.path.exists(cls.monkey_log):
            print('monkey result folder already exists')
        else:
            print('monkey result folder does not exist, automatically created')
            os.mkdir(cls.monkey_log)

    @classmethod
    def create_monkey_result(cls):
        cls.monkey_result_path = os.getcwd() + '/Monkey_log/%s' % get_format_current_time()
        os.mkdir(cls.monkey_result_path)

    # throttle_set : Set the execution time interval in milliseconds
    # seed_set : Set the seed value. If the seed value is the same, the running monkey sequence is the same.
    # perform_times : The number of executions of monkey
    # --pct-motion 30 --pct-trackball 30 --pct-touch 10 --pct-appswitch 10
    def run_monkey(self, seed_set, perform_times):
        self.monkey_log = self.monkey_result_path
        cmd = "adb -s %s shell monkey -p com.nice.main -v -v --throttle 200 -s %s --ignore-crashes --ignore-timeouts --ignore-security-exceptions --monitor-native-crashes %s >%s/%s.log" % (
            self.device.device_id, seed_set, perform_times, self.monkey_log, self.device.device_name)
        subprocess.call(cmd, shell=True)

    # Definition list, this list is used to store the log file name generated by the device
    lis = []

    # Read all files in the current result folder and add the file name of each file to the list
    @classmethod
    def open_filelist(cls):
        cls.pathDir = os.listdir(cls.monkey_result_path)
        for allDir in cls.pathDir:
            child = os.path.join('%s/%s' % (cls.monkey_result_path, allDir))
            cls.lis.append(child)

    anr = 0
    crash = 0
    monkey_total_result = ''

    @classmethod
    def read_log(cls):
        # Create a file that counts crash and anr results, and write to the header
        monkey_total_result = cls.monkey_result_path + "/Summary.txt"
        print('The file name is：%s ' % monkey_total_result)

        init = open(monkey_total_result, 'a+')
        init_log = u'---------Statistics of this monkey test result--------\n'
        init.writelines(init_log)
        init.close()

        # Read the log file of each device
        for currentlis in cls.lis:
            crashfile = open(currentlis, 'rb')

            # Open the statistical result file in a writable way
            monkey_result = open(monkey_total_result, 'a+')
            # Device Information
            result_string = 'file: %s Statistics of crash and anr \n' % currentlis
            monkey_result.writelines(result_string)

            # Loop through each line in the log file
            for s in crashfile.readlines():
                if 'CRASH: com.nice.main' in s:  # Count the number of occurrences of Crash
                    cls.crash = cls.crash + 1
                    crash_line = 'Crash log:\n %s \n' % s
                    monkey_result.writelines(crash_line)
                if 'ANR in com.nice.main' in s:  # Count the number of occurrences of ANR
                    cls.anr = cls.anr + 1
                    anr_line = u'ANR log:\n %s \n' % s
                    monkey_result.writelines(anr_line)
            crashfile.close()

            # crash number
            crash_string = 'Crash statistics: %s \n' % cls.crash
            monkey_result.writelines(crash_string)
            # anr number
            anr_string = 'anr number statistics: %s \n' % cls.anr
            monkey_result.writelines(anr_string)
            # Word wrap
            enter = '\n'
            monkey_result.writelines(enter)
            # Close file
            monkey_result.close()
            # After the file is traversed, the variables of crash and anr are cleared to 0
            cls.crash = 0
            cls.anr = 0
        cls.lis.append(monkey_total_result)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ monkey~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
