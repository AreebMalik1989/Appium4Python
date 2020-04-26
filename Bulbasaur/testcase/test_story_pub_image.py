#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Normal case use case

import sys
import time
from common.BaseTestCase import *
sys.path.append('..')


class TestStoryPubImage(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_001_story_pub_image(self):
        """
        Check the volume keys to take pictures, rear camera, night mode, filters, brushes, text
        """
        # Enter the story shooting page
        self.tester.swipe_right()
        time.sleep(3)

        # Dry the guide floating layer of the story
        for num in range(2):
            self.tester.tap_screen_center()

        if not self.tester.is_element_exist('com.nice.main:id/record_btn', 3):
            self.tester.screenshot('The device does not support story')
            self.tester.press_keycode(4)
        else:
            # Record video with the volume key
            self.tester.start_screen_record('story volume key to take photos')

            # If the device supports beauty mode, click the beauty button
            if self.tester.is_element_exist('com.nice.main:id/beauty_auto'):
                self.tester.find_element_by_id_and_tap('com.nice.main:id/beauty_auto')
            else:
                self.tester.screenshot('Story did not find the beauty button')

            # If the device has night mode, click the night mode button
            if self.tester.is_element_exist('com.nice.main:id/night_mode', 3):
                self.tester.find_element_by_id_and_tap('com.nice.main:id/night_mode')
            else:
                self.tester.screenshot('story did not find the night mode button')

            # Press the volume key to take pictures
            self.tester.press_keycode(25)

            time.sleep(5)

            # Slide switch filter
            for i in range(5):
                self.tester.swipe_right()

            # Stop video recording
            self.tester.stop_screen_record('story volume key to take photos')

            # Click on the brush and draw the brush route
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_draw')
            self.tester.swipe_screen(self.tester.device_width / 4, self.tester.device_height / 4,
                                     self.tester.device_width / 4, self.tester.device_height / 4 * 3)

            # Click on the brush thickness line to adjust the brush thickness
            self.tester.find_element_by_id_and_tap('com.nice.main:id/civ')

            # Click the fluorescent brush and draw the route
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_highlighter')
            time.sleep(3)
            self.tester.swipe_screen(self.tester.device_width / 2, self.tester.device_height / 4,
                                     self.tester.device_width / 2, self.tester.device_height / 4 * 3)

            # Switch the brush color to draw the route
            try:
                self.tester.find_element_by_xpath_and_tap('//android.widget.ImageView[6]')
            except:
                time.sleep(1)

            time.sleep(3)
            self.tester.swipe_screen(self.tester.device_width / 4 * 3, self.tester.device_height / 4,
                                     self.tester.device_width / 4 * 3, self.tester.device_height / 4 * 3)

            # Click OK to exit the brush
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_save')

            # Click on copy and enter copy
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_add_text')
            self.tester.find_element_by_id_and_send_keys('com.nice.main:id/et_story', 'autotest')

            # Click OK to exit the copy editing state
            # self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_save')
            self.tester.press_keycode(4)
            # Story editing results
            self.tester.screenshot('story_picture_editing_results')

            # Click Next to enter the release preview page
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_edit_complete')

            # Handle the guide prompt for entering the preview page for the first time
            if self.tester.is_element_exist('com.nice.main:id/story_scene_info_close', 5):
                self.tester.find_element_by_id_and_tap('com.nice.main:id/story_scene_info_close')

            # Post story
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_post_btn')

            # Waiting to upload stories
            time.sleep(10)

            # Feed page post results
            self.tester.screenshot('story_picture_released')

            # Enter my story to view
            if self.tester.is_element_exist('my_story'):
                self.tester.find_element_by_xpath_and_tap(
                    '//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[2]')
            else:
                self.tester.screenshot('story_did_not_find_my_story')
                return

            self.tester.start_screen_record('story_Check_the_story_I_posted')

            # Handle the problem of looking at story mask
            time.sleep(2)
            if self.tester.is_element_exist('Click_on_both_sides_of_the_screen_to_switch_photos'):
                self.tester.tap_screen_center()

            # Wait for the playback to complete and return to the feed
            if self.tester.is_element_exist('com.nice.main:id/btnTabSubscription', timeout=20):
                self.tester.stop_screen_record('story检查前置拍摄的故事')
            elif self.tester.is_element_exist('com.nice.main:id/img_return'):
                try:
                    self.tester.driver.find_element_by_id('com.nice.main:id/img_return').click()
                except:
                    print("try to tap close button failed")
                self.tester.stop_screen_record('story检查前置拍摄的故事')
            else:
                self.tester.stop_screen_record('story检查前置拍摄的故事')
                self.tester.back_to_feed()

            self.tester.stop_screen_record('story检查我发布的故事')

            # Clean up my published stories
            self.tester.clear_pub_story()
            self.tester.back_to_feed()

    def test_002_story_pub_image(self):
        """
        Check the front camera and take pictures
        """

        # Enter the story shooting page
        self.tester.swipe_right()
        time.sleep(3)

        if not self.tester.is_element_exist('com.nice.main:id/record_btn', 3):
            self.tester.screenshot(u'设备不支持发story')
            self.tester.press_keycode(4)
        else:
            # If the device supports beauty mode, click the beauty button
            if self.tester.is_element_exist('com.nice.main:id/beauty_auto'):
                self.tester.find_element_by_id_and_tap('com.nice.main:id/beauty_auto')
            else:
                self.tester.screenshot(u'story没找到美颜按钮')

            # If the device has night mode, click the night mode button
            if self.tester.is_element_exist('com.nice.main:id/night_mode'):
                self.tester.find_element_by_id_and_tap('com.nice.main:id/night_mode')
                self.tester.screenshot(u'story没找到夜间模式按钮')

            # Record video with the volume key
            self.tester.start_screen_record(u'story前置摄像头音量键拍摄照片')

            # Switch the camera to the front
            self.tester.find_element_by_id_and_tap('com.nice.main:id/switch_camera')
            time.sleep(5)

            # Press the volume key to take pictures
            self.tester.press_keycode(25)

            # Wait for the photo to finish
            self.tester.wait_element('com.nice.main:id/story_draw')

            # Stop video recording
            self.tester.stop_screen_record(u'story前置摄像头音量键拍摄照片')

            # Story editing results
            self.tester.screenshot(u'storystory前置摄像头编辑结果')

            # Click Next to enter the release preview page
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_edit_complete')
            time.sleep(4)

            # Post story
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_post_btn')

            # Click feed
            time.sleep(10)
            self.tester.wait_element('com.nice.main:id/btnTabSubscription')

            # Feed page post results
            self.tester.screenshot(u'storystory发布完成')

            # Enter my story to view
            if self.tester.is_element_exist(u'我的故事'):
                self.tester.find_element_by_xpath_and_tap(
                    '//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[2]')
            else:
                self.tester.screenshot(u'story未找到我的故事')
                return

            self.tester.start_screen_record(u'story检查前置拍摄的故事')

            # Wait for the playback to complete and return to the feed
            if self.tester.is_element_exist('com.nice.main:id/btnTabSubscription', timeout=20):
                self.tester.stop_screen_record(u'story检查前置拍摄的故事')
            elif self.tester.is_element_exist('com.nice.main:id/img_return'):
                try:
                    self.tester.driver.find_element_by_id('com.nice.main:id/img_return').click()
                except:
                    print("try to tap close button failed")
                self.tester.stop_screen_record(u'story检查前置拍摄的故事')
            else:
                self.tester.stop_screen_record(u'story检查前置拍摄的故事')
                self.tester.back_to_feed()

            # Clean up my published stories
            self.tester.clear_pub_story()
            self.tester.back_to_feed()

    def test_003_story_pub_image(self):
        """
        Check non-music filters for photos, filters, text, brushes
        """
        # Enter the story shooting page
        self.tester.swipe_right()
        time.sleep(3)

        if not self.tester.is_element_exist('com.nice.main:id/record_btn', 3):
            self.tester.screenshot(u'设备不支持发story')
            self.tester.press_keycode(4)
        else:
            self.tester.find_element_by_id_and_tap('com.nice.main:id/lens_enter')
            time.sleep(15)

            # Find the coordinates of the center point of the filter control on the right side of the shooting button, click
            element = self.tester.driver.find_element_by_xpath(
                '//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[5]')
            self.tester.get_center_coor_and_tap(element)
            time.sleep(4)

            # Click to take a photo
            self.tester.find_element_by_id_and_tap('com.nice.main:id/record_btn')

            time.sleep(5)

            # Slide switch filter
            for i in range(0, 5):
                self.tester.swipe_right()

            # Click on the brush and draw the brush route
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_draw')
            time.sleep(3)
            self.tester.swipe_screen(self.tester.device_width / 4, self.tester.device_height / 4,
                                     self.tester.device_width / 4, self.tester.device_height / 4 * 3)

            # Click on the brush thickness line to adjust the brush thickness
            self.tester.find_element_by_id_and_tap('com.nice.main:id/civ')

            # Click the fluorescent brush and draw the route
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_highlighter')
            time.sleep(3)
            self.tester.swipe_screen(self.tester.device_width / 2, self.tester.device_height / 4,
                                     self.tester.device_width / 2, self.tester.device_height / 4 * 3)

            # Switch the brush color to draw the route
            try:
                self.tester.find_element_by_xpath_and_tap('//android.widget.ImageView[6]')
            except:
                time.sleep(1)

            time.sleep(3)
            self.tester.swipe_screen(self.tester.device_width / 4 * 3, self.tester.device_height / 4,
                                     self.tester.device_width / 4 * 3, self.tester.device_height / 4 * 3)

            # Click OK to exit the brush
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_save')

            # Click on copy and enter copy
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_add_text')
            self.tester.find_element_by_id_and_send_keys('com.nice.main:id/et_story', 'autotest')

            # Click OK to exit the copy editing state
            # self.tester.find_element_by_id_and_tap('com.nice.main:id/btn_save')
            self.tester.press_keycode(4)

            # Story editing results
            self.tester.screenshot(u'storystory非音乐滤镜图片编辑结果')

            # Click Next to enter the release preview page
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_edit_complete')
            time.sleep(4)

            # Handle the guide prompt for entering the preview page for the first time
            if self.tester.is_element_exist('com.nice.main:id/story_scene_info_close'):
                self.tester.find_element_by_id_and_tap('com.nice.main:id/story_scene_info_close')

            # Post story
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_post_btn')

            # Click feed
            self.tester.wait_element('com.nice.main:id/btnTabSubscription')

            # Feed page post results
            self.tester.screenshot(u'storystory非音乐滤镜图片发布完成')

            # Waiting to upload stories
            time.sleep(5)

            # Enter my story to view
            if self.tester.is_element_exist(u'我的故事'):
                self.tester.find_element_by_xpath_and_tap(
                    '//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[2]')
            else:
                self.tester.screenshot(u'story未找到我的故事')
                return

            self.tester.start_screen_record(u'story检查非音乐滤镜拍摄的故事')

            if self.tester.is_element_exist(u'点击屏幕两侧切换照片', timeout=5):
                self.tester.tap_screen_center()

            # Wait for the playback to complete and return to the feed
            if self.tester.is_element_exist('com.nice.main:id/btnTabSubscription', timeout=100):
                self.tester.stop_screen_record(u'story检查非音乐滤镜拍摄的故事')
            elif self.tester.is_element_exist('com.nice.main:id/img_return'):
                try:
                    self.tester.driver.find_element_by_id('com.nice.main:id/img_return').click()
                except:
                    print("try to tap close button failed")
                self.tester.stop_screen_record(u'story检查非音乐滤镜拍摄的故事')
            else:
                self.tester.stop_screen_record(u'story检查非音乐滤镜拍摄的故事')
                self.tester.back_to_feed()

            # Clean up my published stories
            self.tester.clear_pub_story()
            self.tester.back_to_feed()

    def test_004_story_pub_image(self):
        """
        Check music filters to take pictures and post
        """
        # Enter the story shooting page
        self.tester.swipe_right()
        time.sleep(3)

        if not self.tester.is_element_exist('com.nice.main:id/record_btn', 3):
            self.tester.screenshot(u'设备不支持发story')
            self.tester.press_keycode(4)
        else:
            # Click to expand lens filter
            self.tester.find_element_by_id_and_tap('com.nice.main:id/lens_enter')
            time.sleep(15)

            # Find the first lens filter click
            self.tester.find_element_by_xpath_and_tap(
                '//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[5]')
            time.sleep(2)
            # Find EDM Music Filter Click
            self.tester.find_element_by_xpath_and_tap(
                '//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[7]')
            time.sleep(4)

            # Click to take a photo
            self.tester.find_element_by_id_and_tap('com.nice.main:id/record_btn')

            # Wait for the photo to finish
            self.tester.wait_element('com.nice.main:id/story_draw')

            # Story editing results
            self.tester.screenshot(u'storystory音乐滤镜图片编辑结果')

            # Click Next to enter the release preview page
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_edit_complete')
            time.sleep(4)

            # Handle the guide prompt for entering the preview page for the first time
            if self.tester.is_element_exist('com.nice.main:id/story_scene_info_close'):
                self.tester.find_element_by_id_and_tap('com.nice.main:id/story_scene_info_close')

            # Post story
            self.tester.find_element_by_id_and_tap('com.nice.main:id/story_post_btn')

            # Click feed
            self.tester.wait_element('com.nice.main:id/btnTabSubscription')

            # Feed page post results
            self.tester.screenshot(u'storystory音乐滤镜图片发布完成')

            # Waiting to upload stories
            time.sleep(5)

            # Enter my story to view
            if self.tester.is_element_exist(u'我的故事'):
                self.tester.find_element_by_xpath_and_tap(
                    '//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[2]')
            else:
                self.tester.screenshot(u'story未找到我的故事')
                return

            self.tester.start_screen_record(u'story检查音乐滤镜拍摄的故事')

            if self.tester.is_element_exist(u'点击屏幕两侧切换照片', timeout=5):
                self.tester.tap_screen_center()

            # Wait for the playback to complete and return to the feed
            if self.tester.is_element_exist('com.nice.main:id/btnTabSubscription', timeout=100):
                self.tester.stop_screen_record(u'story检查音乐滤镜拍摄的故事')
            elif self.tester.is_element_exist('com.nice.main:id/img_return'):
                try:
                    self.tester.driver.find_element_by_id('com.nice.main:id/img_return').click()
                except:
                    print("try to tap close button failed")
                self.tester.stop_screen_record(u'story检查音乐滤镜拍摄的故事')
            else:
                self.tester.stop_screen_record(u'story检查音乐滤镜拍摄的故事')
                self.tester.back_to_feed()

            # Clean up my published stories
            self.tester.clear_pub_story()
            self.tester.back_to_feed()

    def tearDown(self):
        pass
        # self.tester.back_to_feed()
        # self.tester.clean_mp4_file()

    # Please reset to feed page
    @classmethod
    def tearDownClass(cls):
        pass
