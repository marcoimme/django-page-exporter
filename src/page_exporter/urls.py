from django.conf.urls import url
from page_exporter.views import capture

urlpatterns = [
    url(r'^', capture, name='capture')
]
