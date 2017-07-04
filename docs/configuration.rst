.. include:: globals
.. _install:


=============
Configuration
=============



How to use
----------


The followings SETTINGS should contain values as follow:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'page_exporter',
        ...
    )


url.py should contain:

.. code-block:: python

    urlpatterns = patterns(
        ...
        (r'^capture/', include('page_exporter.urls')),
        ...
    )

you can ovverride default configuration using:

.. code-block:: python

    PAGE_EXPORTER_CAPTURE_SCRIPT = './capture.js'
    PAGE_EXPORTER_CLI_ARGS = []
    PAGE_EXPORTER_PHANTOMJS_CMD = None
    PAGE_EXPORTER_WAIT = '2000'
    PAGE_EXPORTER_TIMEOUT = '60000'