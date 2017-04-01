# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import django_webtest
import pytest

default = object()

ADMIN = 'admin'
PWD = '123'

@pytest.fixture(scope='function')
def app(request):
    wtm = django_webtest.WebTestMixin()
    wtm.csrf_checks = False
    wtm._patch_settings()
    request.addfinalizer(wtm._unpatch_settings)
    return django_webtest.DjangoTestApp()
