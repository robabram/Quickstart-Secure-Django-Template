#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

#
# Setup Admin user and configure Oauth.
# Run: 'python manage.py admin --init-oauth' after running database migration.
#

import sys
import copy
from enum import Enum

from oauth2_provider.models import Application
from oauth2_provider.generators import ClientIdGenerator, ClientSecretGenerator

from django.contrib.auth.models import User
from django.conf import settings
from proj.settings.base import ADMIN_ACCOUNT_NAME, ADMIN_ACCOUNT_PASSWORD


LJ_SIZE = 70


class ColorType(Enum):

    ok = 1
    info = 2
    warning = 3
    error = 4


class OauthSetup(object):

    options = None
    model = None
    first_boot = False

    def color_string(self, data, type):
        """
        Add color statements to string
        :param str: string to colorize
        :param type: ColorType enum value
        :return: colorized string
        """

        # http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python

        if self.options['no_color']:
            return data

        CEND = '\x1b[0m'

        if type == ColorType.ok:
            return '\x1b[1;32;40m{0}{1}'.format(data, CEND)
        if type == ColorType.error:
            return '\x1b[1;31;40m{0}{1}'.format(data, CEND)
        if type == ColorType.warning:
            return '\x1b[1;36;40m{0}{1}'.format(data, CEND)
        if type == ColorType.info:
            return '\x1b[1;34;40m{0}{1}'.format(data, CEND)

        return str

    def print_ok(self):
        sys.stdout.write('[{0}]\n'.format(self.color_string('Ok', ColorType.ok)))

    def print_error(self):
        sys.stdout.write('[{0}]\n'.format(self.color_string('Err', ColorType.error)))

    def print_no(self, type):
        sys.stdout.write('[{0}]\n'.format(self.color_string('No', type)))

    def print_yes(self, type):
        sys.stdout.write('[{0}]\n'.format(self.color_string('Yes', type)))

    def admin_user_exists(self):
        """
        Check to see if the admin user record exists in the database
        :return: True if yes, otherwise False
        """
        try:
            User.objects.get(username='admin')
        except User.DoesNotExist:
            return False

        return True

    def create_admin_user(self):
        """
        Create the project admin user
        :return: True if user exists, False if not
        """

        sys.stdout.write('creating admin user...'.ljust(LJ_SIZE))

        User.objects.create_superuser(username=ADMIN_ACCOUNT_NAME, password=ADMIN_ACCOUNT_PASSWORD, email='')
        self.print_ok()

        return self.admin_user_exists()

    def oauth_app_exists(self):
        """
        Check to see if the oauth2 application has been configured
        :return: True if yes, otherwise False
        """
        try:
            Application.objects.get(name=settings.OAUTH2_APPLICATION_NAME)
        except Application.DoesNotExist:

            return False

        return True

    def create_oauth_app(self):
        """
        Check to see if the oauth2 application has been configured
        :return: True if yes, otherwise False
        """

        sys.stdout.write('configuring up oauth...'.ljust(LJ_SIZE))

        u = User.objects.get(username='admin')

        client_id = ClientIdGenerator().hash()
        secret = ClientSecretGenerator().hash()

        Application.objects.create(
            client_id=client_id,
            client_type='confidential',
            redirect_uris='',
            authorization_grant_type='password',
            client_secret=secret,
            name=settings.OAUTH2_APPLICATION_NAME,
            user_id=u.id,
            skip_authorization=0
        )

        self.print_ok()

        return True

    def handle(self, options):

        self.options = copy.deepcopy(options)

        self.first_boot = not self.admin_user_exists()

        #
        # Check admin user exists
        #
        sys.stdout.write('checking if admin user exists...'.ljust(LJ_SIZE))
        if not self.admin_user_exists():
            self.print_no(ColorType.warning)
            if not self.create_admin_user():
                sys.stdout.write(
                    self.color_string('failed to create admin account', ColorType.error))
        else:
            self.print_yes(ColorType.ok)

        #
        # Check OAuth configuration
        #
        sys.stdout.write('checking if oauth has been configured...'.ljust(LJ_SIZE))
        if not self.oauth_app_exists():
            self.print_no(ColorType.warning)
            self.create_oauth_app()
        else:
            self.print_yes(ColorType.ok)

        #
        # Verify that the admin user id matches the oauth user id value
        #
        sys.stdout.write('verifying admin account oauth settings are correct...'.ljust(LJ_SIZE))
        if User.objects.get(username='admin').id != \
                    Application.objects.get(name=settings.OAUTH2_APPLICATION_NAME).user_id:
            self.print_no(ColorType.warning)
            sys.stdout.write(
                self.color_string('The oauth settings for the admin account are not correct!', ColorType.error))
        else:
            self.print_yes(ColorType.ok)

