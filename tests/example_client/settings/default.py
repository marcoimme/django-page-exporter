import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = '=k(c2*!w1j=(*e)j#!sm&-juc-a(m)vr-226bil(d(#kz_280j'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, 'templates'),
]

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'page_exporter',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)

LOGIN_URL = '/'
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
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'exampleopenidclient',
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


from .logging_conf import *  # noqa
