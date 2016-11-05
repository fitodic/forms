# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite3'),
    }
}


ALLOWED_HOSTS += ['127.0.0.1', 'localhost']

RUNSERVERPLUS_SERVER_ADDRESS_PORT = '127.0.0.1:8000'

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

try:
    import django_extensions
    INSTALLED_APPS += ['django_extensions']
except ImportError:
    pass

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_ROOT, 'debug.log'),
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'locallogger': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'qinspect': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
