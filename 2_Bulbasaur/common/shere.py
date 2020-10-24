#!/usr/bin/env python3
# -*- coding:utf-8 -*-


class GlobalVar:

    run_mode = 'autotest'
    if_run = False  # Was there a task running at the time
    task_id = 0  # Current task id


def set_run_mode(value):
    GlobalVar.run_mode = value


def get_run_mode():
    return GlobalVar.run_mode


def set_if_run(value):
    GlobalVar.if_run = value


def get_if_run():
    return GlobalVar.if_run


def set_task_id(value):
    GlobalVar.task_id = value


def get_task_id():
    return GlobalVar.task_id
