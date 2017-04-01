from django.utils import six
import os
import logging
import subprocess
from tempfile import NamedTemporaryFile
import json
from mimetypes import guess_type, guess_all_extensions
try:
    from urllib.parse import urljoin
except ImportError:
    # Python 2
    from urlparse import urljoin
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator
from page_exporter.config import conf


logger = logging.getLogger(__name__)


class UnsupportedImageFormat(Exception):
    pass


class CaptureError(Exception):
    pass


def phantomjs_command_kwargs():
    """ will construct kwargs for cmd
    """
    kwargs = {
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
        'universal_newlines': True
    }
    phantom_js_cmd = conf.PHANTOMJS_CMD
    if phantom_js_cmd:
        path = '{0}:{1}'.format(os.getenv('PATH', ''), phantom_js_cmd)
        kwargs.update({'env': {'PATH': path}})
    return kwargs


def phantomjs_command():
    cmd = conf.PHANTOMJS_CMD
    cmd = [cmd]

    # Concatenate with capture script
    app_path = os.path.dirname(__file__)

    capture = conf.CAPTURE_SCRIPT
    if capture.startswith('./'):
        capture = os.path.join(app_path, 'scripts', capture)

    assert os.path.exists(capture), 'Cannot find %s' % capture
    return cmd + [capture]


PHANTOMJS_CMD = phantomjs_command()


def page_capture(stream, url, method=None, width=None, height=None,
                 selector=None, data=None, waitfor=None, size=None,
                 crop=None, render='png', wait=None, cookie_name=None, cookie_value=None, cookie_domain=None,
                 page_status=None):
    """
    Captures web pages using ``phantomjs``
    """
    if isinstance(stream, six.string_types):
        output = stream
    else:
        with NamedTemporaryFile('wb+', suffix='.%s' % render, delete=False) as f:
            output = f.name
    try:
        cmd = PHANTOMJS_CMD + [url, output]

        # Extra command-line options
        cmd += ['--format=%s' % render]
        if method:
            cmd += ['--method=%s' % method]
        if width:
            cmd += ['--width=%s' % width]
        if height:
            cmd += ['--height=%s' % height]
        if selector:
            cmd += ['--selector=%s' % selector]
        if data:
            cmd += ['--data="%s"' % json.dumps(data)]
        if waitfor:
            cmd += ['--waitfor=%s' % waitfor]
        if wait:
            cmd += ['--wait=%s' % wait]
        if cookie_name:
            cmd += ['--cookie_name=%s' % cookie_name]
        if cookie_value:
            cmd += ['--cookie_value=%s' % cookie_value]
        if cookie_domain:
            cmd += ['--cookie_domain=%s' % cookie_domain]
        if page_status:
            cmd += ['--page_status=%s' % page_status]
        logger.debug(cmd)
        # Run PhantomJS process
        proc = subprocess.Popen(cmd, **phantomjs_command_kwargs())
        stdout = proc.communicate()[0]
        process_phantomjs_stdout(stdout)

        size = parse_size(size)
        render = parse_render(render)

        if size or (render and render != 'png' and render != 'pdf'):
            # pdf isn't an image, therefore we can't postprocess it.
            image_postprocess(output, stream, size, crop, render)
        else:
            if stream != output:
                # From file to stream
                with open(output, 'rb') as out:
                    stream.write(out.read())
                stream.flush()
    finally:
        if stream != output:
            os.unlink(output)


def process_phantomjs_stdout(stdout):
    """Parse and digest capture script output.
    """
    for line in stdout.splitlines():
        bits = line.split(':', 1)
        if len(bits) < 2:
            bits = ('INFO', bits)
        level, msg = bits

        if level == 'FATAL':
            logger.fatal(msg)
            raise CaptureError(msg)
        elif level == 'ERROR':
            logger.error(msg)
        else:
            logger.info(msg)


def image_mimetype(render):
    render = parse_render(render)
    # All most web browsers don't support 'image/x-ms-bmp'.
    if render == 'bmp':
        return 'image/bmp'
    return guess_type('foo.%s' % render)[0]


def parse_url(request, url):
    """Parse url URL parameter."""
    try:
        validate = URLValidator()
        validate(url)
    except ValidationError:
        if url.startswith('/'):
            host = request.get_host()
            scheme = 'https' if request.is_secure() else 'http'
            url = '{scheme}://{host}{uri}'.format(scheme=scheme,
                                                  host=host,
                                                  uri=url)
        else:
            url = request.build_absolute_uri(reverse(url))
    return url


def parse_render(render):
    formats = {
        'jpeg': guess_all_extensions('image/jpeg'),
        'png': guess_all_extensions('image/png'),
        'gif': guess_all_extensions('image/gif'),
        'bmp': guess_all_extensions('image/x-ms-bmp'),
        'tiff': guess_all_extensions('image/tiff'),
        'xbm': guess_all_extensions('image/x-xbitmap'),
        'pdf': guess_all_extensions('application/pdf')
    }
    if not render:
        render = 'png'
    else:
        render = render.lower()
        for k, v in formats.items():
            if '.%s' % render in v:
                render = k
                break
        else:
            render = 'png'
    return render


def parse_size(size_raw):

    try:
        width_str, height_str = size_raw.lower().split('x')
    except AttributeError:
        size = None
    except ValueError:
        size = None
    else:
        try:
            width = int(width_str)
            assert width > 0
        except (ValueError, AssertionError):
            width = None
        try:
            height = int(height_str)
            assert height > 0
        except (ValueError, AssertionError):
            height = None
        size = width, height
        if not all(size):
            size = None
    return size


def image_postprocess(imagefile, output, size, crop, render):
    """
    Resize and crop captured image, and saves to output.
    (can be stream or filename)
    """
    try:
        from PIL import Image
    except ImportError:
        import Image

    img = Image.open(imagefile)
    size_crop = None
    img_resized = img
    if size and crop and crop.lower() == 'true':
        width_raw, height_raw = img.size
        width, height = size
        height_better = int(height_raw * (float(width) /
                                          width_raw))
        if height < height_better:
            size_crop = (0, 0, width, height)

    try:
        if size_crop:
            size_better = width, height_better
            img_better = img.resize(size_better, Image.ANTIALIAS)
            img_resized = img_better.crop(size_crop)
        elif size:
            img_resized = img.resize(size, Image.ANTIALIAS)

        # If save with 'bmp' use default mode('RGBA'), it will raise:
        # "IOError: cannot write mode RGBA as BMP".
        # So, we need convert image mode
        # from 'RGBA' to 'RGB' for 'bmp' format.
        if render == 'bmp':
            img_resized = img_resized.convert('RGB')
        # Fix IOError: cannot write mode RGBA as XBM
        elif render == 'xbm':
            img_resized = img_resized.convert('1')
        # Works with either filename or file-like object
        img_resized.save(output, render)
    except KeyError:
        raise UnsupportedImageFormat
    except IOError as e:
        raise CaptureError(e)


# def build_absolute_uri(request, url):
#     """
#     Allow to override printing url, not necessarily on the same
#     server instance.
#     """
#     if conf.CAPTURE_ROOT_URL:
#         return urljoin(conf.CAPTURE_ROOT_URL, url)
#     return request.build_absolute_uri(url)
