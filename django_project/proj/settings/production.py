#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

# Celery bombs if the import doesn't work
try:
    from proj.settings.base import *
except ImportError:
    from django_project.proj.settings.base import *  # Celery requires this import

PRODUCTION = True
#
# Security Settings -
#     !!! RUN: python manage.py admin --init-production !!!
#     This will change settings in this file, including generating new keys below.
#
# SECURITY WARNING: keep the secret key used in production secret.
SECRET_KEY = '_^!%+93zs%x2^7n!vh3-qou&zr_3_!cq8i$_a^-0lq7esmtfvd'
# Fernet Key is used for encrypting and decrypting the oauth token cookie.
FERNET_KEY = b'womHVQpPQ0Kj9yqTnB1RmKGTWaaTpJ7EFsB8wQR0P6M='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1', '[::1]']
ALLOWED_INCLUDE_ROOTS = (BASE_DIR, '/home', '/var/www/html/')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
