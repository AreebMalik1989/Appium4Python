#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from common.BaseTestCase import *


class TestCaseManager:

    def __init__(self, tester):
        self.tester = tester
        self.compatibility_suite = unittest.TestSuite()
        self.testcase_class = []
        self.load_case()

    def load_case(self):
        testcase_array = []
        test_suits = unittest.defaultTestLoader.discover('testcase/', pattern='test*.py')
        for test_suite in test_suits:
            for suite in test_suite._tests:
                for test in suite:
                    testcase_array.append(test.__class__)
        self.testcase_class = sorted(set(testcase_array), key=testcase_array.index)

    # Compatibility test cases
    def compatibility_test_suite(self):
        for testcase in self.testcase_class:
            self.compatibility_suite.addTest(BaseTestCase.parametrize(testcase, tester=self.tester))
        return self.compatibility_suite

    # monkey automation
    def monkey_android(self):
        self.tester.run_monkey(200, 1000)

    # Functional test case
    def functional_test_suite(self):
        pass

    def signal_case_suit(self, test_my_class):
        suite = unittest.TestSuite()
        suite.addTest(BaseTestCase.parametrize(test_my_class, tester=self.tester))
        return suite
