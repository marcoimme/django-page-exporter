import mock
import subprocess
from django.http import HttpResponseBadRequest
from django.test import RequestFactory

from page_exporter.views import capture

try:
    from django.urls import reverse_lazy
except:
    from django.core.urlresolvers import reverse_lazy
from fixtures import *  # NOQA



@mock.patch.object(subprocess, 'Popen', autospec=True)
def test_view_capture(mock_popen):
    mock_popen.return_value.returncode = 0
    mock_popen.return_value.communicate.return_value = ("output", "Error")
    p = {
        'url': 'http://example.com',
        'render': 'png',
        'cookie_name': 'test',
        'cookie_value': 'test',
        'cookie_domain': 'test',
        'width': 100,
        'height': 100,
        'page_status': 'test',
        'method': 'test',
        'selector': 'test',
        'data': {"a": "b"},
        'waitfor': 'test',
        'wait': 'test',
    }
    rf = RequestFactory()
    request = rf.get(reverse_lazy('capture'), p)
    capture(request)
    assert mock_popen.called

@mock.patch.object(subprocess, 'Popen', autospec=True)
def test_view_capture_badRequest(mock_popen):
    mock_popen.return_value.returncode = 0
    mock_popen.return_value.communicate.return_value = ("output", "Error")
    rf = RequestFactory()
    p = {}
    request = rf.get(reverse_lazy('capture'), p)
    ret = capture(request)
    assert isinstance(ret, HttpResponseBadRequest)

    p = {
        'url': 'badurl'
    }
    request = rf.get(reverse_lazy('capture'), p)
    ret = capture(request)
    assert isinstance(ret, HttpResponseBadRequest)


@mock.patch.object(subprocess, 'Popen', autospec=True)
def test_view_capture_wrong_size_params(mock_popen):
    mock_popen.return_value.returncode = 0
    mock_popen.return_value.communicate.return_value = ("output", "Error")
    rf = RequestFactory()
    p = {
        'url': 'http://example.com',
        'width': 'aa',
        'height': 'bb',
    }
    request = rf.get(reverse_lazy('capture'), p)
    ret = capture(request)
    args, kwargs = mock_popen.call_args
    assert '--width=aa' not in args[0]
    assert '--height=bb' not in args[0]


@mock.patch.object(subprocess, 'Popen', autospec=True)
def test_view_capture_wrong_size_params(mock_popen):
    mock_popen.return_value.returncode = 0
    mock_popen.return_value.communicate.return_value = ("output", "Error")
    rf = RequestFactory()
    p = {
        'url': 'http://example.com',
        'width': 'aa',
        'height': 'bb',
    }
    request = rf.get(reverse_lazy('capture'), p)
    ret = capture(request)
    args, kwargs = mock_popen.call_args
    assert '--width=aa' not in args[0]
    assert '--height=bb' not in args[0]
