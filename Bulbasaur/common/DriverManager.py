#!/usr/bin/env python3
# -*- coding:utf-8 -*-


class DriverManager:

    drivers = {}

    # Quit all Drivers
    @classmethod
    def quit_all_driver(cls):
        print(cls.drivers)
        for device_id, driver in cls.drivers.items():
            if driver:
                print(driver)
                driver.quit()

    # Exit the corresponding Driver according to device_id
    @classmethod
    def quit_driver(cls, device_id):
        if device_id in cls.drivers.keys():
            if cls.drivers[device_id]:
                cls.drivers[device_id].quit()
