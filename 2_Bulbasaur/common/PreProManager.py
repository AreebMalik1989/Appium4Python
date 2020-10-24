#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from prepro.ASUSZ00APreProcess import *
from prepro.ChuiZi_YQ607PreProcess import *
from prepro.Coopad8729PreProcess import *
from prepro.Coopad8729blackPreprocess import *
from prepro.Coopad8765PreProcess import *
from prepro.HTCBFPreProcess import *
from prepro.HTCD826wPreProcess import *
from prepro.HTCONEPreProcess import *
from prepro.HUIWEIP6PreProcess import *
from prepro.HuaWeiJAZZProPrecess import *
from prepro.LeX620PreProcess import *
from prepro.LianXiang5860PreProcess import *
from prepro.LianXiangK30TPreProcess import *
from prepro.M3notePreProcess import *
from prepro.M57APreProcess import *
from prepro.MEITU5PreProcess import *
from prepro.MEITUM4PreProcess import *
from prepro.MEIZU4PROPreProcess import *
from prepro.MX5PreProcess import *
from prepro.MZM1notePreProcess import *
from prepro.MZM2NotePreProcess import *
from prepro.Nexus6PreProcess import *
from prepro.ONEPlusXPreProcess import *
from prepro.OPPOA33PreProcess import *
from prepro.OPPOA37PreProcess import *
from prepro.OPPOA59PreProcess import *
from prepro.OPPON5207PreProcess import *
from prepro.OPPOR7sPreProcess import *
from prepro.OPPOR8700PreProcess import *
from prepro.OPPOR9PreProcess import *
from prepro.RedMi1sPreProcess import *
from prepro.RedMi2APreProcess import *
from prepro.RedMiNote2PreProcess import *
from prepro.RedMiNote3PreProcess import *
from prepro.RedMiNote4PreProcess import *
from prepro.Smartisan1PreProcess import *
from prepro.Smartisan705PreProcess import *
from prepro.SumSing9152PreProcess import *
from prepro.SumSingNote3PreProcess import *
from prepro.SumSingNote4PreProcess import *
from prepro.SumSingS4PreProcess import *
from prepro.VIVOV3MAXPreProecss import *
from prepro.VIVOX5ProPreProcess import *
from prepro.VivoX7PreProcess import *
from prepro.XIAOMI2PreProcess import *
from prepro.XIAOMI3PreProcess import *
from prepro.XIAOMI4PreProcess import *
from prepro.XIAOMI5PreProcess import *
from prepro.XIAOMINOTEPreProcess import *


class PreProManager(object):

    def __init__(self, tester):
        self.tester = tester
        self.device_id = self.tester.device.device_id

    def device(self):
        if self.device_id == "5HUC9S6599999999":
            return OPPOR9PreProcess(self.tester)
        elif self.device_id == "7c404969":
            return OPPOA33PreProcess(self.tester)
        elif self.device_id == "G6Q4U4EA99999999":
            return OPPOA37PreProcess(self.tester)
        elif self.device_id == "810EBL22MGP3":
            return MZM2NotePreProcess(self.tester)
        elif self.device_id == "LJYTZ5D699999999":
            return RedMiNote2PreProcess(self.tester)
        elif self.device_id == "LE66A06250102401":
            return LeX620PreProcess(self.tester)
        elif self.device_id == "MIAGLMC6A2100083":
            return MEITU5PreProcess(self.tester)
        elif self.device_id == "RCKVVCSO99999999":
            return OPPOA59PreProcess(self.tester)
        elif self.device_id == "4TEI7DK799999999":
            return RedMiNote3PreProcess(self.tester)
        elif self.device_id == "4d00f31dba19a02d":
            return SumSingS4PreProcess(self.tester)
        elif self.device_id == "a42516eb":
            return XIAOMINOTEPreProcess(self.tester)
        elif self.device_id == "bef9e460":
            return LianXiangK30TPreProcess(self.tester)
        elif self.device_id == 'ee72d34d':
            return SumSingNote3PreProcess(self.tester)
        elif self.device_id == 'b33aa57c':
            return XIAOMI5PreProcess(self.tester)
        elif self.device_id == 'A10ABNN76XMP':
            return M57APreProcess(self.tester)
        elif self.device_id == '4c4bb164':
            return XIAOMI2PreProcess(self.tester)
        elif self.device_id == '0021119e':
            return XIAOMI3PreProcess(self.tester)
        elif self.device_id == '022BTF7N43046595':
            return HUAWEIP6PreProcess(self.tester)
        elif self.device_id == '76UBBKR224R8':
            return MEIZU4PROPreProcess(self.tester)
        elif self.device_id == '91QEBPL694VC':
            return M3notePreProcess(self.tester)
        elif self.device_id == 'HT53WWZ02029':
            return HTCBFPreProcess(self.tester)
        elif self.device_id == 'HT53DYJ00008':
            return HTCONEPreProcess(self.tester)
        elif self.device_id == 'K21GAMN5A1901310':
            return MEITUM4PreProcess(self.tester)
        elif self.device_id == 'ZX1G22HQSB':
            return Nexus6PreProcess(self.tester)
        elif self.device_id == 'VCOZHE6L99999999':
            return VIVOX5ProPreProcess(self.tester)
        elif self.device_id == 'HEPBPF4D49S4FUGY':
            return OPPOR7sPreProcess(self.tester)
        elif self.device_id == '174034d3':
            return VIVOV3MAXPreProcess(self.tester)
        elif self.device_id == '91QEBP63ULCD':
            return M3notePreProcess(self.tester)
        elif self.device_id == '179323c4':
            return Coopad8729PreProcess(self.tester)
        elif self.device_id == '71MBBL622EG3':
            return MZM1notePreProcess(self.tester)
        elif self.device_id == '27ba3598':
            return ONEPlusXPreProcess(self.tester)
        elif self.device_id == '410ac5dd9036c000':
            return SumSing9152PreProcess(self.tester)
        elif self.device_id == '8d994efc':
            return VivoX7ProPreProcess(self.tester)
        elif self.device_id == '3DN4C16411014042':
            return HuaWeiG9PreProcess(self.tester)
        elif self.device_id == 'CC53DYG03271':
            return HTCD826wPreProcess(self.tester)
        elif self.device_id == 'b3e5b28e':
            return XIAOMI4PreProcess(self.tester)
        elif self.device_id == 'e80c9403':
            return RedMi1sPreProcess(self.tester)
        elif self.device_id == '8526c60c':
            return SumSingNote4PreProcess(self.tester)
        elif self.device_id == 'P4M0215418001139':
            return HUAWEIMT7PreProcess(self.tester)
        elif self.device_id == 'd9b28b5c':
            return Smartisan705Process(self.tester)
        elif self.device_id == 'F8AZFG01U429':
            return ASUSZ00APreProcessPreProcess(self.tester)
        elif self.device_id == 'ZLWOUCWKLNT4AMKN':
            return RedMiNote4PreProcess(self.tester)
        elif self.device_id == '8c9847a5':
            return Smartosan1PreProcess(self.tester)
        elif self.device_id == '54da7023':
            return OPPON5207PreProcess(self.tester)
        elif self.device_id == '9418d864':
            return OPPOR8700PreProcess(self.tester)
        elif self.device_id == '2a2ac28':
            return Coopad8765PreProcess(self.tester)
        elif self.device_id == 'b8939c4':
            return Coopad8729blackPreprocess(self.tester)
        elif self.device_id == '179323c4':
            return Coopad8729PreProcess(self.tester)
        elif self.device_id == '85UABM7HEBC2':
            return MX5PreProcess(self.tester)
        elif self.device_id == 'd0a9661f':
            return Smartosan1PreProcess(self.tester)
        elif self.device_id == 'V6V7N14C01000156':
            return HuaWeiJAZZProPrecess(self.tester)
        elif self.device_id == 'HGC9GXBJ':
            return LianXiang5860PreProcess(self.tester)
        elif self.device_id == '6O5528A28423':
            return RedMi2APreProcess(self.tester)
        elif self.device_id == 'e249ecb3':
            return ChuiZi_YQ607PreProcess(self.tester)
