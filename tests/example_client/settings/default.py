import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = '=k(c2*!w1j=(*e)j#!sm&-juc-a(m)vr-226bil(d(#kz_280j'
DEBUG = True
ALLOWED_HOSTS = ['*']

SESSION_COOKIE_NAME = 'example_client'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'page_exporter',
    'example_client',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = "/private/"

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'example_client.urls'
WSGI_APPLICATION = 'example_client.wsgi.application'
SITE_ID = 1
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'exampleclient.db',
        # 'TEST_NAME': 'db1111111.sqlite3',
        'USER': 'postgres',
        'PASSWORD': ''
    }
}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

STATICFILES_DIRS = [
    os.path.join(os.path.dirname(__file__), '..', 'static'),
]

PAGE_EXPORTER_PHANTOMJS_CMD = os.path.join(os.path.dirname(__file__), '..', 'phantomjs', 'phantomjs')
PAGE_EXPORTER_PHANTOMJS_CMD = 'node'

PAGE_EXPORTER_CAPTURE_SCRIPT = './print.js'

PAGE_EXPORTER_WAIT = '10000'
# PAGE_EXPORTER_CLI_ARGS = ['--ignore-ssl-errors=true', '--ssl-protocol=any']

from .logging_conf import *  # noqa
