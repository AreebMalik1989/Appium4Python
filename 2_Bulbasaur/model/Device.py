#!/usr/bin/env python3
# -*- coding:utf-8 -*-


class Device:

    def __init__(self, device_id):
        self._device_id = device_id
        self._device_name = ""
        self._platform_version = ""
        self._platform_name = ""
        self._bootstrap_port = ""
        self._server_port = ""
        self._server = ""

    @property
    def device_id(self):
        return self._device_id

    @device_id.setter
    def device_id(self, value):
        self._device_id = value

    @property
    def device_name(self):
        return self._device_name

    @device_name.setter
    def device_name(self, value):
        self._device_name = value

    @property
    def platform_version(self):
        return self._platform_version

    @platform_version.setter
    def platform_version(self, value):
        self._platform_version = value

    @property
    def platform_name(self):
        return self._platform_name

    @platform_name.setter
    def platform_name(self, value):
        self._platform_name = value

    @property
    def bootstrap_port(self):
        return self._bootstrap_port

    @bootstrap_port.setter
    def bootstrap_port(self, value):
        self._bootstrap_port = value

    @property
    def server_port(self):
        return self._server_port

    @server_port.setter
    def server_port(self, value):
        self._server_port = value

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, value):
        self._server = value
