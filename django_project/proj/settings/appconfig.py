#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

#
# Handle Django signals
#

from django.apps import AppConfig
from django.db.models.signals import pre_save, post_save, pre_delete, post_migrate


def signal_post_migrate_callback(**kwargs):
    """ Actions to do after a migrate command has completed """

    # print('post migration signal received')
    pass


class AppTemplateConfig(AppConfig):
    """
    # https://docs.djangoproject.com/en/1.11/ref/signals/#module-django.db.backends
    """

    name = 'django_project'
    verbose_name = 'Django Project'

    def ready(self):

        # from proj.signals import signal_model_pre_save, signal_model_post_save, signal_model_pre_delete

        # pre_save.connect(signal_model_pre_save)
        # pre_delete.connect(signal_model_pre_delete)

        post_migrate.connect(signal_post_migrate_callback)

        pass