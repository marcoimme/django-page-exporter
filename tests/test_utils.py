import pytest
import urllib
from io import BytesIO

import mock as mock
import subprocess

from django.http import HttpResponseBadRequest
from django.test import RequestFactory
try:
    from django.urls import reverse, NoReverseMatch
except:
    from django.core.urlresolvers import reverse, NoReverseMatch

from page_exporter.utils import phantomjs_command_kwargs, phantomjs_command, image_mimetype, parse_render, parse_size, \
    page_capture, parse_url
from page_exporter.views import capture


def test_phantomjs_command_kwargs():
    kw = phantomjs_command_kwargs()
    assert 'stdout' in kw
    assert 'stderr' in kw
    assert 'universal_newlines' in kw
    assert 'env' in kw


def test_phantomjs_command():
    out = phantomjs_command()
    assert 'phantomjs' in out[0]
    assert 'capture' in out[1]


def test_image_mimetype():
    assert image_mimetype(None) == 'image/png'
    assert image_mimetype('jpg') == 'image/jpeg'
    assert image_mimetype('png') == 'image/png'
    assert image_mimetype('xbm') == 'image/x-xbitmap'
    assert image_mimetype('bmp') == 'image/bmp'
    assert image_mimetype('notvalid') == 'image/png'


def test_parse_render():
    assert parse_render(None) == 'png'
    assert parse_render('jpg') == 'jpeg'
    assert parse_render('html') == 'png'
    assert parse_render('gif') == 'gif'
    assert parse_render('pdf') == 'pdf'
    assert parse_render('notvalid') == 'png'


def test_parse_size():
    assert parse_size('aa') is None
    assert parse_size((100,None)) is None
    assert parse_size('300x100') == (300, 100)
    assert parse_size('300x') is None
    assert parse_size('x100') is None
    assert parse_size('x') is None


@mock.patch.object(subprocess, 'Popen', autospec=True)
def test_parse_url(mock_popen):
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
    request = rf.get(reverse('capture'), p)

    assert parse_url(request, '/tmp') == 'http://testserver/tmp'
    assert parse_url(request, 'capture') == 'http://testserver/e/'

    with pytest.raises(NoReverseMatch):
        parse_url(request, 'nonamedurl')

    assert parse_url(request, 'http://example.com') == 'http://example.com'


@mock.patch.object(subprocess, 'Popen', autospec=True)
def test_page_capture_base(mock_popen):
    mock_popen.return_value.returncode = 0
    mock_popen.return_value.communicate.return_value = ("output", "Error")
    stream = BytesIO()
    page_capture(stream, 'http://example.com')
    assert mock_popen.called


@mock.patch.object(subprocess, 'Popen', autospec=True)
def test_page_capture_with_params(mock_popen):
    mock_popen.return_value.returncode = 0
    mock_popen.return_value.communicate.return_value = ("output", "Error")
    stream = BytesIO()

    p = {
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

    page_capture(stream, 'http://example.com', **p)
    assert mock_popen.called

    args, kwargs = mock_popen.call_args
    assert '--format=png' in args[0]
    assert '--cookie_name=test' in args[0]
    assert '--cookie_value=test' in args[0]
    assert '--cookie_domain=test' in args[0]
    assert '--width=100' in args[0]
    assert '--height=100' in args[0]
    assert '--page_status=test' in args[0]
    assert '--method=test' in args[0]
    assert '--selector=test' in args[0]
    assert '--data="{"a": "b"}"' in args[0]
    assert '--waitfor=test' in args[0]
    assert '--wait=test' in args[0]

    assert kwargs == phantomjs_command_kwargs()
