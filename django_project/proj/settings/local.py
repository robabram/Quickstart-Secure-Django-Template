#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

from proj.settings.base import *

#
# Logging
#
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'website.log',
            'formatter': 'verbose',
            'maxBytes': 1024 * 1000 * 100  # 100MB
        },
        'lockout': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'lockout.log',
            'formatter': 'verbose',
            'maxBytes': 1024 * 1000 * 100  # 100MB
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],   # Could change to: ['null'],
            'level': 'ERROR',  # Change this to DEBUG to see SQL Queries in log output
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'axes.watch_login': {
            'handlers': ['lockout'],
            'propagate': False,
            'level': 'INFO',
        },
        'celery': {
            'handlers': ['console'],
            'propagate': False,
            'level': os.getenv('DJANGO_LOG_LEVEL', 'WARNING'),
        },
    }
}

