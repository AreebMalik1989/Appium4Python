#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import unittest


class BaseTestCase(unittest.TestCase):

    def __init__(self, method_name='runTest', tester=None):
        super(BaseTestCase, self).__init__(method_name)
        self.tester = tester

    @staticmethod
    def parametrize(testcase_klass, tester=None):
        test_loader = unittest.TestLoader()
        test_names = test_loader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in test_names:
            suite.addTest(testcase_klass(name, tester=tester))
        return suite
