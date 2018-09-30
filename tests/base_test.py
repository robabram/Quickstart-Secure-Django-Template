#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase
from oauth2_provider.models import get_application_model
from oauth2_provider.settings import oauth2_settings
from testfixtures import LogCapture

from proj.common.oauth_helper import create_access_token
from proj.settings.base import ADMIN_ACCOUNT_NAME, ADMIN_ACCOUNT_PASSWORD

Application = get_application_model()
UserModel = get_user_model()


class BaseTest(TestCase):
    def setUp(self):
        self.log = LogCapture()

        self.test_user = get_user_model().objects.create_user(ADMIN_ACCOUNT_NAME, "admin@example.com",
                                                              ADMIN_ACCOUNT_PASSWORD)
        self.test_user.save()
        self.test_user.profile.oauth_scope = 'read write'
        self.test_user.profile.accepted_terms = True
        self.test_user.profile.account_activated = True
        self.test_user.profile.save()

        self.application = Application(
            name="django_project",
            redirect_uris="http://localhost http://example.com http://example.it",
            user=self.test_user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )
        self.application.save()

        mysite = Site.objects.get_current()
        mysite.name = 'Django-Project'
        mysite.save()

        oauth2_settings._SCOPES = ['read', 'write', 'groups']

        # Use the helper to create the access token and refresh token db records.
        self.token = create_access_token(self.test_user, self.test_user.profile.oauth_scope)

    def tearDown(self):
        self.application.delete()
        self.test_user.delete()
        self.log.uninstall()


