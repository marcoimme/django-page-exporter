# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging

from django.conf import settings
from django.views.generic.base import ContextMixin, TemplateView


class PrivateView(TemplateView):
    template_name = 'private.html'

    def get_context_data(self, **kwargs):
        cookie_name = getattr(settings, 'SESSION_COOKIE_NAME', 'sessionid')
        kwargs['cookie_name'] = cookie_name
        kwargs['cookie_value'] = self.request.COOKIES.get(cookie_name, '')
        kwargs['cookie_domain'] = 'localhost'
        return super(PrivateView, self).get_context_data(**kwargs)