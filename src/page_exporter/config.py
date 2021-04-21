# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals


PAGE_EXPORTER_CAPTURE_SCRIPT = './capture.js'
PAGE_EXPORTER_CLI_ARGS = []
PAGE_EXPORTER_SCRIPT_CMD = None
PAGE_EXPORTER_WAIT = '2000'
PAGE_EXPORTER_TIMEOUT_SECONDS = 60
PAGE_EXPORTER_NODE_PATH = None
PAGE_EXPORTER_ENVIRON = {}


class Settings(object):
    def __init__(self, prefix):
        self.prefix = prefix

    def __getattr__(self, item):
        target = "{}_{}".format(self.prefix, item)
        try:
            from django.conf import settings as django_settings
            return getattr(django_settings, target, globals()[target])
        except Exception:
            return globals()[target]


conf = Settings('PAGE_EXPORTER')
