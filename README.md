Django Page Exporter
==============================

Simple Django application to export web pages in different formats (png, jpeg, pdf...)

See https://django-page-exporter.readthedocs.org/en/latest/ for detailed documentation on the project.

[![Build Status](https://travis-ci.org/marcoimme/django-page-exporter.svg?branch=develop)](https://travis-ci.org/marcoimme/django-page-exporter)
[![codecov](https://codecov.io/gh/marcoimme/django-page-exporter/branch/develop/graph/badge.svg)](https://codecov.io/gh/marcoimme/django-page-exporter)

How to use
----------
Install django-page-exporter:

    pip install django-page-exporter


Include page_exporter in your SETTINGS as follow:

    INSTALLED_APPS = (
        ...
        'page_exporter',
        ...
    )

url.py should contain:

    urlpatterns = patterns(
        ...
        (r'^capture/', include('page_exporter.urls')),
        ...
    )

Following SETTINGS are available:

    PAGE_EXPORTER_CAPTURE_SCRIPT = './capture.js'
	PAGE_EXPORTER_PHANTOMJS_CMD = '~/bin/phantomjs'
	PAGE_EXPORTER_WAIT = '2000'
	PAGE_EXPORTER_TIMEOUT_SECONDS = 60

See [docs](https://django-page-exporter.readthedocs.org/en/latest/) for further information


Start coding
------------
    make develop

Tests
------------
    make test

Running Local
-------------
    make init
    make demo
