#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import datetime
import os
import re


def get_format_current_time():
    current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
    return current_time


def get_full_file_from_path(path, ext=None):
    allfiles = []
    need_ext_filter = (ext is not None)
    for root, dirs, files in os.walk(path):
        for files_path in files:
            file_path = os.path.join(root, files_path)
            extension = os.path.splitext(file_path)[1][1:]
            if need_ext_filter and extension in ext:
                allfiles.append(file_path)
            elif not need_ext_filter:
                allfiles.append(file_path)
    return allfiles


def get_file_name_from_path(path, ext=None):
    all_file_names = []
    need_ext_filter = (ext is not None)
    for root, dirs, files in os.walk(path):
        for files_path in files:
            filename, suffix = os.path.splitext(files_path)
            extension = os.path.splitext(files_path)[1][1:]
            if need_ext_filter and extension in ext:
                all_file_names.append(filename)
            elif not need_ext_filter:
                all_file_names.append(filename)
    return all_file_names


def clean_brackets_from_str(string):
    final_string = re.sub(r'[\(（][\s\S]*[\)）]', "", string)
    return final_string


def read_file(filename, mode):
    f = open(filename, mode)  # filename, file path, name, if \, pay attention to escape or add r at the beginning, mode read mode, r read, w write
    read = f.read()  # Get content and store in variable
    print(read)
    f.close()  # close files and save memory
