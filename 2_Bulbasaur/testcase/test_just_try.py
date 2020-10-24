#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys

from model.Tester import *
from common.BaseTestCase import *

sys.path.append('..')


class TestLongPress(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_longpress_0(self):
        print("Beauty")

    def test_longpress_1(self):
        time.sleep(5)
        self.tester.back_to_feed()
        print("Return feed")

    # Active skip case
    def test_longpress_2(self):
        time.sleep(1)
        self.skipTest("hahha")

    # Fail case
    def test_longpress_3(self):
        time.sleep(1)
        self.fail("manual")

    def test_longpress_4(self):
        time.sleep(1)
        print("End 4 ~~~~~")

    def tearDown(self):
        pass

    # Please reset to feed page
    @classmethod
    def tearDownClass(cls):
        pass
