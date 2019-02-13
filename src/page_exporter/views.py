import logging
from io import BytesIO

try:  # Django>=2
    from django.urls.exceptions import NoReverseMatch
except:  # NOQA
    from django.core.urlresolvers import NoReverseMatch
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.translation import ugettext as _

from page_exporter.config import conf
from page_exporter.utils import (page_capture, CaptureError, UnsupportedImageFormat,
                    image_mimetype, parse_url)

logger = logging.getLogger(__name__)


def capture(request):
    # Merge both QueryDict into dict
    parameters = dict([(k, v) for k, v in request.GET.items()])
    parameters.update(dict([(k, v) for k, v in request.POST.items()]))
    url = parameters.get('url')
    html_content = parameters.get('html')
    if not url and not html_content:
        return HttpResponseBadRequest(_('Missing url or html parameter'))

    if url:
        try:
            url = parse_url(request, url)
        except NoReverseMatch:
            error_msg = _("URL '%s' invalid (could not reverse)") % url
            return HttpResponseBadRequest(error_msg)
    # if html_content:
    #     html_content = "\"{}\"".format(html_content)

    method = parameters.get('method', request.method)
    selector = parameters.get('selector')
    data = parameters.get('data')
    waitfor = parameters.get('waitfor')
    wait = parameters.get('wait', conf.WAIT)
    render = parameters.get('render', 'png')
    size = parameters.get('size')
    crop = parameters.get('crop')
    cookie_name = parameters.get('cookie_name')
    cookie_value = parameters.get('cookie_value')
    cookie_domain = parameters.get('cookie_domain')
    page_status = parameters.get('page_status')
    landscape = parameters.get('landscape', 'false')

    try:
        width = int(parameters.get('width', ''))
    except ValueError:
        width = None
    try:
        height = int(parameters.get('height', ''))
    except ValueError:
        height = None

    stream = BytesIO()
    try:
        page_capture(stream, url or html_content, method=method.lower(), width=width,
                     height=height, selector=selector, data=data,
                     size=size, waitfor=waitfor, crop=crop, render=render,
                     wait=wait, cookie_name=cookie_name, cookie_value=cookie_value,
                     cookie_domain=cookie_domain, page_status=page_status, landscape=landscape)
    except CaptureError as e:
        return HttpResponseBadRequest(e)
    except ImportError:
        error_msg = _('Resize not supported (PIL not available)')
        return HttpResponseBadRequest(error_msg)
    except UnsupportedImageFormat:
        error_msg = _('Unsupported image format: %s' % render)
        return HttpResponseBadRequest(error_msg)

    response = HttpResponse(content_type=image_mimetype(render))
    response.write(stream.getvalue())

    return response
