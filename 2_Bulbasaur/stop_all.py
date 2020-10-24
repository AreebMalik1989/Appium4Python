#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


def stop_appium():
    r = os.popen("ps -ef | grep appium")
    info = r.readlines()
    for line in info:  # traverse by line
        words = line.split()
        appium_pid = words[1]
        os.popen("kill " + appium_pid)
        print("kill: " + appium_pid)


def kill_server(port):
    cmd = "lsof -i:%s|awk 'NR==2{print $2}'" % port
    pid = os.popen(cmd).read()
    cmd = "kill -9 %s" % pid
    os.popen(cmd).read()


if __name__ == "__main__":
    stop_appium()
    kill_server(8886)
