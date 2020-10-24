#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import collections
import traceback
import unittest

from datetime import datetime

from common.DataProvider import *
from common.PublicMethod import *


class TheTestResult(unittest.TestResult):

    detail_results = {}  # {"5HUC9S6599999999":{},"":{}}
    total_results = {}
    device = {}
    test_result_path = ""
    file_css = ""
    file_js = ""

    def __init__(self, stream=None, descriptions=None, verbosity=None):
        unittest.TestResult.__init__(self, stream=None, descriptions=None, verbosity=None)
        self.logger = Log.logger
        self._test_case_dict = collections.OrderedDict()
        self.if_write_start_time = False
        self.tester = None
        self.device_id = None

    def startTest(self, test):

        self.tester = test.tester
        self.device_id = self.tester.device.device_id
        testcase_start_time = get_format_current_time()
        self.logger.debug('Device：%s Start Run %s' % (self.tester.device.device_name, test))
        print(test.id())

        # Initialize the data structure of the total result of each device
        if self.__class__.total_results.has_key(self.device_id):
            pass
        else:
            self.__class__.total_results[self.device_id] = collections.OrderedDict()
            self.__class__.total_results[self.device_id]['totalrun'] = 0
            self.__class__.total_results[self.device_id]['startime'] = 0
            self.__class__.total_results[self.device_id]['stoptime'] = 0
            self.__class__.total_results[self.device_id]['errortestcase'] = 0
            self.__class__.total_results[self.device_id]['failtestcase'] = 0
            self.__class__.total_results[self.device_id]['skiptestcase'] = 0
            self.__class__.total_results[self.device_id]['successtestcase'] = 0

        # Total number of use cases
        self.__class__.total_results[self.device_id]['totalrun'] = self.__class__.total_results[self.device_id][
                                                                       'totalrun'] + 1

        # Starting time
        if self.if_write_start_time:
            pass
        else:
            self.__class__.total_results[self.device_id]['starttime'] = testcase_start_time
            self.if_write_start_time = True

        # Detailed execution results of each device
        self._test_case_dict[test] = collections.OrderedDict()
        if self.device_id in self.__class__.detail_results.keys():
            pass
        else:
            self.__class__.device[self.device_id] = self.tester.device
            self.__class__.detail_results[self.device_id] = self._test_case_dict
        self.__class__.detail_results[self.device_id][test]['startime'] = testcase_start_time

    def stopTest(self, test):
        testcase_stop_time = get_format_current_time()
        self.logger.debug('device：%s Stop Run %s' % (self.tester.device.device_name, test))
        self.__class__.detail_results[self.device_id][test]['stoptime'] = testcase_stop_time
        testcase_consuming_time = self.__class__.get_time_consuming(
            self.__class__.detail_results[self.device_id][test]['startime']
            , self.__class__.detail_results[self.device_id][test]['stoptime'])
        self.__class__.detail_results[self.device_id][test]['consumingtime'] = testcase_consuming_time
        self.__class__.total_results[self.device_id]['stoptime'] = testcase_stop_time

    def startTestRun(self):
        # self.logger.debug('The test begins...')
        pass

    def stopTestRun(self):
        # self.logger.debug('Finished test...')
        pass

    def addError(self, test, err):
        info = '************      - %s -!(Error)    ***************' % self.tester.device.device_name
        self.logger.warning(info)
        # traceback.print_tb(err[2])
        traceback.print_exc()
        info = 'Error device:%s Run TestCase %s, Error info:%s' % (
            self.tester.device.device_name, test, traceback.format_exception(err[0], err[1], err[2]))
        self.logger.error(info)
        info = '************************************************'
        self.logger.warning(info)

        # Error screenshot
        my_test = str(test)
        simple_name = clean_brackets_from_str(my_test).replace(' ', '')
        my_scr = "Error_%s" % simple_name
        self.tester.screenshot2(my_scr)

        # Error log
        m_list = traceback.format_exception(err[0], err[1], err[2])
        list_err = list()  # The list contains the error log information to be output
        list_err.append(m_list[-1])
        list_err.append(m_list[2])

        if self.device_id in self.__class__.total_results.keys():
            self.__class__.total_results[self.device_id]['errortestcase'] = \
                self.__class__.total_results[self.device_id]['errortestcase'] + 1
        else:
            self.__class__.total_results[self.device_id]['errortestcase'] = 0

        try:
            self.__class__.detail_results[self.device_id][test]['result'] = 'Error'
            self.__class__.detail_results[self.device_id][test]['reason'] = list_err
        except Exception as e:
            info = Exception, ":", e
            self.logger.error(info)

    def addFailure(self, test, err):
        info = '************      - %s -!(Fail)    ***************' % self.tester.device.device_name
        self.logger.warning(info)
        info = 'Fail device:%s Run TestCase %s, Fail info:%s' % (self.tester.device.device_name, test, err[1].message)
        self.logger.warning(info)
        info = '***********************************************'
        self.logger.warning(info)

        # Failure screenshot
        my_test = str(test)
        simple_name = clean_brackets_from_str(my_test).replace(' ', '')
        my_scr = "Failure_%s" % simple_name
        self.tester.screenshot2(my_scr)

        # Failure log
        m_list = traceback.format_exception(err[0], err[1], err[2])
        list_fail = list()  # The list contains the error log information to be output
        list_fail.append(m_list[-1])
        list_fail.append(m_list[2])

        self.__class__.total_results[self.device_id]['failtestcase'] = self.__class__.total_results[self.device_id][
                                                                           'failtestcase'] + 1

        self.__class__.detail_results[self.device_id][test]['result'] = 'Fail'
        self.__class__.detail_results[self.device_id][test]['reason'] = list_fail

    def addSuccess(self, test):
        self.__class__.total_results[self.device_id]['successtestcase'] = self.__class__.total_results[self.device_id][
                                                                              'successtestcase'] + 1

        self.__class__.detail_results[self.device_id][test]['result'] = 'Success'
        self.__class__.detail_results[self.device_id][test]['reason'] = 'No'

    def addSkip(self, test, reason):
        info = '→_→Skip Run TestCase %s, Skip reason:%s' % (test, reason)
        self.logger.debug(info)
        self.__class__.total_results[self.device_id]['skiptestcase'] = self.__class__.total_results[self.device_id][
                                                                           'skiptestcase'] + 1

        self.__class__.detail_results[self.device_id][test]['result'] = 'Skip'
        self.__class__.detail_results[self.device_id][test]['reason'] = reason

    @classmethod
    def get_time_consuming(cls, start_time, end_time):
        start_time = datetime.datetime.strptime(start_time, "%Y_%m_%d_%H:%M:%S")
        end_time = datetime.datetime.strptime(end_time, "%Y_%m_%d_%H:%M:%S")
        time_consuming = end_time - start_time

        if time_consuming.seconds <= 0:
            time_str = '< 1 second'
        else:
            time_str = '%s second' % time_consuming.seconds
        return time_str

    @classmethod
    def create_result_folder(cls):
        cls.test_result_path = os.getcwd() + '/testresult/%s' % get_format_current_time()
        os.mkdir(cls.test_result_path)

    # css file path
    file_css = os.getcwd() + '/testresult/result.css'
    # js file path
    file_js = os.getcwd() + '/testresult/result.js'
    # js file path
    sort_table_js = os.getcwd() + '/testresult/sorttable.js'

    @classmethod
    def generate_html_test_result(cls):
        pass
        """
        page = PyH('测试报告')
        result_title = "nice Auto Test Report"

        # 增加css样式及js脚本
        page.addCSS(cls.filecss)
        page.addJS(cls.filejs)
        page.addJS(cls.sorttablejs)
        homediv = page << div(id='nice_report', cl='nice_header_passed')
        reporttitle = homediv << div(result_title, id='title')

        # 获取apk信息
        apk_name = ApkInfo().get_apk_pkg()
        apk_version_name = ApkInfo().get_apk_version_name()
        apk_version_code = ApkInfo().get_apk_version_code()

        # 展示apk相关信息
        reportsummary = homediv << div(id='summary')
        reportsummary << p(apk_name)
        reportsummary << p(apk_version_code)
        reportsummary << p(apk_version_name)

        tabdiv = page << div(id="Tab1")
        menuboxdiv = tabdiv << div(cl="Menubox")
        contentdiv = tabdiv << div(cl="Contentbox")

        tabul = menuboxdiv << ul()
        index = 1
        size = len(cls.detailresults)
        for deviceid, testresult in cls.detailresults.iteritems():
            tabstr = "setTab('one',%s, %s)" % (index, size)
            liid = "one%s" % index
            if index == 1:
                tabul << li(cls.device[deviceid].device_name, id=liid, onmouseover=tabstr, cl="hover")
            else:
                tabul << li(cls.device[deviceid].device_name, id=liid, onmouseover=tabstr)

            content_div_id = "con_one_%s" % index
            if index == 1:
                detaildiv = contentdiv << div(id=content_div_id, cl="hover")
            else:
                detaildiv = contentdiv << div(id=content_div_id, style="display:none")

            totaldiv = detaildiv << div(id='Total')
            totallabel = totaldiv << p('设备总结果:',align="left")
            totalresulttable = totaldiv << table(cl='totalResult', border="1", cellpadding="15")
            # totalresulttable.attributes['class'] = 'totalResult'
            result_title_tr = totalresulttable << tr()
            result_value_tr = totalresulttable << tr()
            ordertitle = collections.OrderedDict()
            timeconsuming = cls.get_time_consuming(cls.totalresults[deviceid]['starttime'], cls.totalresults[deviceid]['stoptime'])
            ordertitle[u'开始时间'] = DataProvider.start_time[deviceid]
            try:
                ordertitle[u'结束时间'] = DataProvider.stop_time[deviceid]
            except:
                ordertitle[u'结束时间'] = ordertitle[u'开始时间']
                Log.logger.debug('%s stoptime: connect error, use default time instead' % cls.device[deviceid].device_name)

            ordertitle[u'总耗时'] = timeconsuming
            ordertitle[u'总用例数'] = cls.totalresults[deviceid]['totalrun']
            ordertitle[u'成功用例数'] = cls.totalresults[deviceid]['successtestcase']
            ordertitle[u'失败用例数'] = cls.totalresults[deviceid]['failtestcase']
            ordertitle[u'错误用例数'] = cls.totalresults[deviceid]['errortestcase']
            ordertitle[u'跳过用例数'] = cls.totalresults[deviceid]['skiptestcase']

            for title, value in ordertitle.iteritems():
                result_title_tr << td(title)
                temp = result_value_tr << td(value)
                temp.attributes['class'] = title

            detaillabel = detaildiv << p('详细执行结果:',align="left")
            detail_table_title = (u'测试用例', u'开始时间', u'结束时间', u'耗时', u'测试结果', u'原因')
            detailresulttable = detaildiv << table(cl='sortable', width="100%", border="1", cellpadding="2", cellspacing="1", style="table-layout:fixed")
            detail_title_tr = detailresulttable << tr()
            for title in detail_table_title:
                detail_title_tr << td(title)
            for key, values in cls.detailresults[deviceid].iteritems():
                testcasetr = detailresulttable << tr()
                mykey = str(key)
                final_key = clean_brackets_from_str(mykey)
                testcasetr << td(final_key, align='left',width="100%",style="word-break:break-all")
                testcasetr << td(values['startime'])
                testcasetr << td(values['stoptime'])
                testcasetr << td(values['consumingtime'])
                try:
                    testcasetr << td(values['result'])
                except:
                    testcasetr << td('device connect error')
                    Log.logger.debug('%s result: device connect error, use default values instead' % cls.device[deviceid].device_name)
                try:
                    testcasetr << td(values['reason'], width="100%", style="word-break:break-all")
                except:
                    testcasetr << td('session error')
                    Log.logger.debug('%s reason: device connect error, use default values instead' % cls.device[deviceid].device_name)

            # 截图展示
            # 创建新div标签，并赋予id
            screencaplable = detaildiv << div(id='screencap')

            # 添加说明
            screencapdiv = detaildiv << p('截图验证:', align="left")

            # 获取截图文件名及绝对路径
            screecap_path = "%s/%s/" % (cls.testresultpath, cls.device[deviceid].device_name)
            screencap_table_title = get_file_name_from_path(screecap_path, 'png')
            screencap_img_src = get_full_file_from_path(screecap_path, 'png')

            # 创建table
            screencapresulttable = screencapdiv << table(width="auto", border="1", cellpadding="2", cellspacing="1",
                                               style="table-layout:fixed")

            # 描述'title'
            screencap_title_tr = screencapresulttable << tr()
            # 描述'内容'
            screencap = screencapresulttable << tr()

            # 循环写入截图名及对应截图
            for title in screencap_table_title:
                screencap_title_tr << td(title)
            for path in screencap_img_src:
                screencap << td("<img src=%s alt=%s width='170' height='300'> " % (path, title))

            # 视频展示
            # 创建新div标签，并赋予id
            screenrecordlable = detaildiv << div(id='screenrecord')
            screenrecorddiv = detaildiv << p('视频验证:', align="left")

            # 获取视频名字及绝对路径
            screerecord_path = "%s/%s/" % (cls.testresultpath, cls.device[deviceid].device_name)
            screenrecord_table_title = get_file_name_from_path(screerecord_path, 'mp4')
            screenrecord_video_src = get_full_file_from_path(screerecord_path, 'mp4')

            # 创建table
            screenrecordresulttable = screenrecorddiv << table(width="auto", border="1", cellpadding="2", cellspacing="1",
                                               style="table-layout:fixed")
            # 描述'title'
            screenrecord_title_tr = screenrecordresulttable << tr()
            # 描述'内容'
            screenrecord = screenrecordresulttable << tr()

            # 循环写入截图名及对应截图
            for title_video in screenrecord_table_title:
                screenrecord_title_tr << td(title_video)
            for path_video in screenrecord_video_src:
                screenrecord << td("<video width='240' height='320' controls='controls'> "
                                "<source src=%s type='video/mp4' /></video>" % path_video)

            # 添加错误截图信息
            errorlable = detaildiv << div(id='errorrecord')
            errordiv = detaildiv << p('错误截图:', align="left")

            error_path = "%s/%s/" % (cls.testresultpath, cls.device[deviceid].device_name)
            error_table_title = get_file_name_from_path(error_path, 'jpg')
            error_src = get_full_file_from_path(screerecord_path, 'jpg')

            # 创建table
            errorresulttable = errordiv << table(width="auto", border="1", cellpadding="2",
                                                               cellspacing="1",
                                                               style="table-layout:fixed")

            error_title = errorresulttable << tr()
            error_valus = errorresulttable << tr()

            # 循环写入截图名及对应截图
            for title_error in error_table_title:
                error_title << td(title_error)
            for path_error in error_src:
                error_valus << td("<img src=%s alt=%s width='170' height='300'> " % (path_error, title))


            # 循环添加各个设备的tab
            index = index + 1

        #生成测试结果Html文件
        htmltestresultfile = '%s/%s.html' % (cls.testresultpath, get_format_current_time())
        try:
            page.printOut(htmltestresultfile)
        except IOError:
            Log.logger.error('file %s not exist' % htmltestresultfile)
            DriverManager.quit_all_driver()

        else:
            Log.logger.debug(u'测试报告创建成功，路径:%s' % htmltestresultfile)"""


if __name__ == '__main__':
    TheTestResult().generate_html_test_result()
