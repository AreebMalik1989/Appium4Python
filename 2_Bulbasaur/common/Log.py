#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import logging
from logging.handlers import RotatingFileHandler
from .PublicMethod import *


class Log:

    logger = None

    @classmethod
    def create_log_file(cls):
        
        logfile = '%s/%s.log' % (os.path.abspath('./log'), get_format_current_time())

        cls.logger = logging.getLogger(__name__)
        cls.logger.setLevel(logging.DEBUG)

        # File handler
        file_handle = RotatingFileHandler(logfile, maxBytes=50 * 1024 * 1024, backupCount=5, encoding="UTF-8")
        formatter = logging.Formatter('%(asctime)s : %(message)s')
        file_handle.setFormatter(formatter)
        cls.logger.addHandler(file_handle)

        # Console handler
        console = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s : %(message)s')
        console.setFormatter(formatter)
        cls.logger.addHandler(console)


if __name__ == '__main__':
    Log.create_log_file()
    Log.logger.debug('this is a debug msg')
    Log.logger.info('this is an info msg')
