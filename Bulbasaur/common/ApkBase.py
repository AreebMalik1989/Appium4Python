#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import subprocess
import os
from math import floor
from common.DataProvider import DataProvider


class ApkInfo:

    def __init__(self):
        apk_path = DataProvider.niceapk
        self.apk_path = apk_path

    def get_apk_size(self):
        """
        Get the size of the package
        """
        size = floor(os.path.getsize(self.apk_path) / (1024 * 1000))
        return str(size) + "M"

    def get_apk_version(self):
        """
        Get version
        """
        cmd = "aapt dump badging " + self.apk_path + " | grep versionName"
        result = ""
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        if output != "":
            result = output.split()[3].decode()[12:]
        return result

    def get_apk_name(self):
        """
        Get the application name
        """
        cmd = "aapt dump badging " + self.apk_path + " | grep application-label: "
        result = ""
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        if output != "":
            result = output.split()[0].decode()[18:]
        return result

    def get_apk_pkg(self):
        """
        Get package name
        """
        cmd = "aapt dump badging " + self.apk_path + " | grep package:"
        result = ""
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        if output != "":
            result = output.split()[1].decode()[6:-1]
        return result

    def get_apk_version_code(self):
        """
        Get version code
        """
        cmd = "aapt dump badging " + self.apk_path + " | grep package | awk '{print $3}'"
        result = ""
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        if output != "":
            result = output.strip('\r\n')
        return result

    def get_apk_version_name(self):
        """
        Get version name
        """
        cmd = "aapt dump badging " + self.apk_path + " | grep package | awk '{print $4}'"
        result = ""
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        if output != "":
            result = output.strip('\r\n')
        return result
