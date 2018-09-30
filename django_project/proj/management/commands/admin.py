#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

#
# Additional Manage.py commands to manage project.
#
# Command: manage.py admin --init-production
#     Create a new unique Secret Key and Fernet key in production settings file.
#

import os
import random
from cryptography.fernet import Fernet

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from django_project.proj.management.oauth_setup import OauthSetup


class Command(BaseCommand):
    help = 'Manage the {0} admin interface'.format(settings.APPLICATION_NAME.capitalize())

    def add_arguments(self, parser):

        parser.add_argument(
            '--init-production',
            action='store_true',
            dest='init_production',
            default=False,
            help='Initialize the production configuration file',
        )

        parser.add_argument(
            '--init-oauth',
            action='store_true',
            dest='init-oauth',
            default=False,
            help='Initialize the Admin account and configure Oauth',
        )

    def init_production_config(self):
        """
        Initialize the production config file with new keys.
        Only use in a production environment.
        """

        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

        # See if we need to initialize the production configuration file
        if os.path.exists('proj/settings/production.py'):

            with open('proj/settings/production.py') as handle:
                lines = handle.readlines()

            # Loop through lines and create the build archive file
            for x in range(0, len(lines)):

                # Always replace the secret key
                if lines[x].startswith('SECRET_KEY'):
                    lines[x] = "SECRET_KEY = '{0}'\n".format(''.join(
                        [random.SystemRandom().choice(chars) for i in range(50)]
                    ))

                # only replace the fernet key if it hasn't been initialized
                if lines[x].startswith('FERNET_KEY') and '%%fernetkey%%' in lines[x]:
                    lines[x] = "FERNET_KEY = {0}\n".format(Fernet.generate_key())

            with open('proj/settings/production.py', 'w') as handle:
                handle.writelines(lines)

    def handle(self, *args, **options):

        handler = None

        if options['init_production']:
            self.init_production_config()
        elif options['init-oauth']:
            handler = OauthSetup()
        else:
            raise CommandError('no command option specified, for help run "python manage.py admin --help"')

        if handler:
            handler.handle(options)



