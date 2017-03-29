# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import logging

import os


def mkdir(newdir):
    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
    """
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError('a file with the same name as the desired '
                      "dir, '%s', already exists." % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            mkdir(head)
        if tail:
            os.mkdir(newdir)


SCM_DASHBOARD_LOG_DIR = os.environ.get('SCM_DASHBOARD_LOG_DIR', os.path.expanduser(
    '~/logs'))

mkdir(SCM_DASHBOARD_LOG_DIR)


def file_handler(name, level):
    return {
        'level': level,
        'class': 'logging.handlers.RotatingFileHandler',
        'formatter': 'full',
        'filename': os.path.join(SCM_DASHBOARD_LOG_DIR, '%s.log' % name),
    }


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'full': {
            'format': '%(levelname)-8s: %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'verbose': {
            'format': '%(levelname)-8s: %(asctime)s %(name)20s %(message)s'
        },
        'simple': {
            'format': '%(levelname)-8s: %(asctime)s %(name)20s: %(funcName)s %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'errors': file_handler('errors', 'DEBUG'),
        'security': file_handler('security', 'DEBUG'),
        'business': file_handler('business', 'DEBUG'),
        'root': file_handler('messages', 'DEBUG'),
        'application': file_handler('page_exporter', 'DEBUG'),
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['root'],
            'level': 'ERROR',
            'propagate': True
        },
        'django.db.backends': {
            'handlers': ['root'],
            'level': 'ERROR',
            'propagate': True
        },
        'errors': {
            'handlers': ['errors'],
            'level': 'ERROR',
            'propagate': True
        },
        'exceptions': {
            'handlers': ['errors'],
            'level': 'ERROR',
            'propagate': True
        },
        'security': {
            'handlers': ['security'],
            'level': 'INFO',
            'propagate': False
        },
        'testing': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'raven': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'celery.task': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

LOGGING_DEBUG = {
    'version': 1,
    'disable_existing_loggers': True,
}

logging.captureWarnings(True)
