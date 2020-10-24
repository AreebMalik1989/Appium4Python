#!usr/bin/python
# -*- coding:utf-8 -*-

from .OPPOR9PreProcess import *


# Processing process is the same as OPPOR9, so directly inherit OPPOR9 processing class
class OPPOA37PreProcess(OPPOR9PreProcess):

    def __init__(self, tester):
        super(OPPOA37PreProcess, self).__init__(tester)
