from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


urlpatterns = [
    # '',
    url(r'^$', TemplateView.as_view(template_name='login.html'), name='login'),

    url(r'private/$', login_required(TemplateView.as_view(template_name='private.html'))),

    url(r'^e/', include('page_exporter.urls')),

    url(r'^admin/', include(admin.site.urls)),
]
