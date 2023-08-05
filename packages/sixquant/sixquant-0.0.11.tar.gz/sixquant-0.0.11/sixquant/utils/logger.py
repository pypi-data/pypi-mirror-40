# coding=utf-8

import os
import logging.config

urllib3_log = logging.getLogger("urllib3")
urllib3_log.setLevel(logging.WARNING)
urllib3_log.propagate = False

requests_log = logging.getLogger("requests")
requests_log.addHandler(logging.NullHandler())
requests_log.propagate = False

matplotlib_log = logging.getLogger("matplotlib")
matplotlib_log.setLevel(logging.WARNING)
matplotlib_log.propagate = False

class Logger(object):
    _logging_conf = __file__[:len(__file__) - len('logger.py')] + '../logging.conf'
    if os.path.exists(_logging_conf):
        logging.config.fileConfig(_logging_conf)

    def __init__(self):
        self.verbose = False

    def config(self, fname, defaults=None, disable_existing_loggers=True):
        logging.config.fileConfig(fname, defaults=defaults, disable_existing_loggers=disable_existing_loggers)

    def get(self, name=None):
        return logging.getLogger(name)


logger = Logger()
