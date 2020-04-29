#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import socketserver
import json
import threading
import http.server as simple_http_server
import urllib.parse as urlparse
import common.share as share

from builtins import _PathLike
from typing import Tuple, Optional, Union

from .RunTestManager import *


class HttpServerHandler(simple_http_server.SimpleHTTPRequestHandler):

    run_manager = None

    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer,
                 directory: Optional[Union[str, _PathLike[str]]]):
        super().__init__(request, client_address, server, directory)
        self.logger = Log.logger
        self.task_id = None

    def end_headers(self):
        self.send_my_headers()
        simple_http_server.SimpleHTTPRequestHandler.end_headers(self)

    def send_my_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")

    def do_POST(self):
        self.logger.debug("--------- POST ---------")

    def do_GET(self):

        self.logger.debug("--------- GET ---------")
        self.logger.debug(self.path)
        parsed_params = urlparse.urlparse(self.path)
        query_parsed = urlparse.parse_qs(parsed_params.query)

        if parsed_params.path == '/run':
            self.run(query_parsed)
        else:
            result_dict = {'code': 1001, "data": {"message": "Bad Command"}}
            self.set_response(result_dict)

    def run(self, params):

        if share.get_if_run():
            result_dict = {'code': 1002, "data": {"message": "There is already a task executing",
                                                  "taskid": "%s" % share.get_task_id()}}
            self.set_response(result_dict)
            return

        if 'mode' in params.keys() is False:
            result_dict = {'code': 1003, "data": {"message": "missing mode parameter"}}
            self.set_response(result_dict)
            return

        elif params['mode'][0] != "monkey" and params['mode'][0] != 'autotest':
            self.set_response({'code': 1004, "data": {"message": "mode parameter error"}})
            return

        try:
            set_run_manager(RunTestManager(params['mode'][0]))
            self.task_id = get_run_manager().task_id
            share.set_task_id(get_run_manager().task_id)  # Set global shared taskid
            share.set_if_run(True)
            thread = threading.Thread(target=get_run_manager().start_run)
            thread.start()
            result_dict = {'code': 0,
                           "data": {"task id fuck": "%s" % self.task_id, "message": "Begin execution %s task" % params['mode']}}
            self.set_response(result_dict)
        except Exception as e:
            traceback.print_exc()
            get_run_manager().stop_run()

    def set_response(self, text, code=200):

        try:
            result = json.dumps(text, ensure_ascii=False)
        except Exception as e:
            traceback.print_exc()
            result = text
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(result)


def get_run_manager():
    return HttpServerHandler.run_manager


def set_run_manager(value):
    HttpServerHandler.run_manager = value
