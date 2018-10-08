#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

"""
Django settings for django_project project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

PRODUCTION = False

# Application name, should mirror project directory name
APPLICATION_NAME = 'django_project'
# Title for swagger API documentation pages
SWAGGER_DOCS_TITLE = 'Django Project API'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.realpath(os.path.dirname(__file__) + "/.."))
ROOT_URLCONF = 'proj.urls'
LOGIN_REDIRECT_URL = '/dashboard/'

# This is the initial admin user account, which is required for setting up Oauth.
# After running 'manage.py migrate' run: 'manage.py admin --init-oauth' to
# create admin user and setup Oauth2 tokens in database.
ADMIN_ACCOUNT_NAME = 'admin'
ADMIN_ACCOUNT_PASSWORD = 'password'

# Quick-start development settings - DO NOT USE THESE KEYS IN PRODUCTION!
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# http://stackoverflow.com/questions/4664724/distributing-django-projects-with-unique-secret-keys
# http://stackoverflow.com/questions/4664724/distributing-django-projects-with-unique-secret-keys/16630719#16630719
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6$^=!bqi132t%wya8_jl0k@6@20#aiat+j0=!!ns-1k&z6t125'

# FERNET Key is used for encrypting and decrypting the oauth token cookie.
# Generate new key with Fernet.generate_key(). https://cryptography.io/en/latest/fernet/
# SECURITY WARNING: keep the fernet key used in production secret!
FERNET_KEY = 'KDTpOti8O-jswRl3zs4GSTqhODHyazk7cxqxG3_39zg='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'proj.settings.appconfig.AppTemplateConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'axes',
    'compressor',
    'timezone_field',
    'proj',
    'apps.accounts',
    'apps.dashboard',
    'apps.api_example',
    'rest_framework_swagger',
    'rest_framework',
    'oauth2_provider',
    'django_celery_results',
]

MIDDLEWARE = [
    'proj.middleware.ThreadLocalMiddleware',
    'proj.middleware.OAuthTokenCookieMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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
                'proj.context_processors.can_edit_processor',
            ],
        },
    },
]

#
# Database Settings for Sqlite3 database
#
DATABASE_NAME = APPLICATION_NAME + '.db'
DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_NAME)

# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_PATH,
    }
}

# If you get the "Error: 1071, 'Specified key was too long; max key length is 767 bytes'"
# when running migrate look at: https://github.com/celery/django-celery/issues/259
CELERY_RESULT_BACKEND = 'django-db'

# https://django-axes.readthedocs.io/en/latest/configuration.html#known-configuration-problems
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'axes_cache': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

# User profile specific timezone activation per request happens in proj/common/oauth_helper.py
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
# USE_THOUSAND_SEPARATOR = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static-prod/')

# Add our root static directory
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

#
# Required for compressor
#
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

#
# WSGI Settings
#
WSGI_APPLICATION = 'proj.wsgi.application'

#
# User Profile Model
#
AUTH_PROFILE_MODULE = "accounts.UserProfile"

#
# django-axes config.  See: https://github.com/django-pci/django-axes/
#
AXES_LOGIN_FAILURE_LIMIT = 10
AXES_USE_USER_AGENT = True
AXES_COOLOFF_TIME = 1
AXES_VERBOSE = False
AXES_CACHE = 'axes_cache'
# AXES_LOCKOUT_TEMPLATE =
# AXES_LOCKOUT_URL =

#
# OAuth2
#
OAUTH2_APPLICATION_NAME = APPLICATION_NAME
# Force re-login X seconds after initial login
OAUTH2_LOGIN_TIMEOUT = 14400

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'api-nodes': 'API Nodes scope',
        'app-all': 'API All scope',
    },
    'ACCESS_TOKEN_EXPIRE_SECONDS': 1800,
}

REST_FRAMEWORK = {

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'proj.api_authentication.APIAuthentication',
        # !!! We are leaving these out, if necessary NodeAuthentication will call them manually.
        # 'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_VERSION': '1.0',
    'DEFAULT_PERMISSION_CLASSES': [
        'proj.api_authentication.APIAuthentication',
        # 'rest_framework.permissions.AllowAny',
        # !!! We are leaving these out, if necessary NodeAuthentication will call them manually.
        # 'rest_framework.permissions.IsAuthenticated',
        # 'oauth2_provider.ext.rest_framework.TokenHasReadWriteScope',
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer'
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}
