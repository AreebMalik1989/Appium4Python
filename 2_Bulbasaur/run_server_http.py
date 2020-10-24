#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from socketserver import ThreadingTCPServer
from common.HttpServerHandler import *
from Server.Server import *
from common import DataProvider, DeviceManager


def kill_server(port):

    cmd = "lsof -i:%s|awk 'NR==2{print $2}'" % port
    pid = os.popen(cmd).read()

    cmd = "kill -9 %s" % pid
    os.popen(cmd).read()


def start_server():

    host = "127.0.0.1"
    port = 8886
    address = (host, port)

    kill_server(port)

    Log.logger.debug('Start Server...')
    server = ThreadingTCPServer(address, HttpServerHandler)
    server.serve_forever()


def main(args=None):

    # Initialize log configuration
    Log.create_log_file()

    Log.logger.info ("Load device and user configuration information")
    DataProvider.init_data()

    Log.logger.info ("Get the device to be tested on the server")
    DeviceManager.get_server_test_device()

    if len(DeviceManager.serverdevices) == 0:
        Log.logger.info ("There is no device to test on the server")
        sys.exit()
    else:
        for device_id, device in DeviceManager.serverdevices.items():
            server = Server(device)
            server.list_connect_devices()

    start_server()


if __name__ == '__main__':
    main()
