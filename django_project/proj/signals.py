#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

#
# Signal handlers for model change events, see: proj.settings.appconfig.
# These are a great way to log user activity.
#

from datetime import datetime

from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

from proj.middleware import get_current_user

# These are apps that should not be remotely logged
LOGGING_EXCLUDED_APPS = (
    'auth',
    'axes',
    'oauth2_provider',
)

# These are models that should not be remotely logged
LOGGING_EXCLUDED_MODELS = (
    'AccessLog',
    'User',
    'SystemActions',
)

# These are model fields that should not be remotely logged
LOGGING_EXCLUDED_FIELDS = (
    'id',
    'http_passwd',
)


def signal_model_pre_save(sender, instance, **kwargs):
    pass


def signal_model_post_save(sender, instance, **kwargs):
    pass


def signal_model_pre_delete(sender, instance, **kwargs):
    pass
