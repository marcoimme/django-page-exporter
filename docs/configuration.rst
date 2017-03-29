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


