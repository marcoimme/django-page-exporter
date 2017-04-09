.. include:: globals
.. _contents:


===================
Parameters
===================

You can then obtain a screenshot using the following GET or POST parameters :

.. toctree::
   :maxdepth: 5

**url**

The website URL to capture. This can be a fully qualified URL, or the name of a URL to be reversed in your Django project. Note: do not forget to encode the url.

**selector**

CSS3 selector. It will restrict the screenshot to the selected element.

**method**

HTTP method to be used (default: GET)

**width**

Viewport width (default: 1400)

**height**

Viewport height (default: 900)

**data**

HTTP data to be posted (default: {})

**wait**

milliseconds used as timeout before capture

**page_status**

string. The screenshot will be performed only once document.page_status is equal to the passed value. Typical usage: if your page contains a heavy javascript processing, you can add the page_status variable at the end of the processing to make sure the screenshot will get the page properly rendered.

**render**

png (default), pdf (will use media print css), jpg (PIL needed)

**cookie_name, cookie_value, cookie_domain**

cookie information to send for authenticated pages