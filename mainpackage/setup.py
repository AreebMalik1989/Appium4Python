from appium import webdriver
from abc import ABC, abstractmethod
from mainpackage.util.configutil import YamlConfigReader


config_reader = YamlConfigReader()
config = config_reader.get_config()


class DriverFactory:

    def get_driver(self):
        if str(config.get('platform').get('selectedPlatform')).lower() == 'android':
            return self._get_android_driver()
        elif str(config.get('platform').get('selectedPlatform')).lower() == 'ios':
            return self._get_ios_driver()
        else:
            raise NotImplementedError

    @staticmethod
    def _get_android_driver():
        cap = dict()
        cap['platformName'] = str(config.get('platform').get('android').get('platformName'))
        cap['platformVersion'] = str(config.get('platform').get('android').get('platformVersion'))
        cap['deviceName'] = str(config.get('platform').get('android').get('deviceName'))
        cap['udid'] = str(config.get('platform').get('android').get('udid'))
        cap['app'] = str(config.get('platform').get('android').get('app'))
        cap['automationName'] = str(config.get('platform').get('android').get('automationName'))
        cap['appActivity'] = str(config.get('platform').get('android').get('appActivity'))
        cap['autoGrantPermissions'] = bool(str(config.get('platform').get('android').get('autoGrantPermissions')))
        cap['autoAcceptAlerts'] = bool(str(config.get('platform').get('android').get('autoAcceptAlerts')))
        cap['noReset'] = bool(str(config.get('platform').get('android').get('noReset')))
        cap['disableWindowAnimation'] = bool(str(config.get('platform').get('android').get('disableWindowAnimation')))
        cap['newCommandTimeout'] = int(str(config.get('platform').get('android').get('newCommandTimeout')))
        cap['waitForIdleTimeout'] = int(str(config.get('platform').get('android').get('waitForIdleTimeout')))

        return webdriver.Remote(str(config.get('platform').get('server')), desired_capabilities=cap)

    @staticmethod
    def _get_ios_driver():
        cap = dict()
        pass
