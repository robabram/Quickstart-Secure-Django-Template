#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#



from django.urls import reverse
from oauth2_provider.models import get_application_model

from apps.accounts.views import login_view
from proj.common.oauth_helper import encrypt_access_token, decrypt_access_token, is_access_token_valid, \
    refresh_access_token
from proj.settings.base import ADMIN_ACCOUNT_NAME, ADMIN_ACCOUNT_PASSWORD
from tests.base_test import BaseTest

ApplicationModel = get_application_model()


# Django Oauth2 tests: https://github.com/evonove/django-oauth-toolkit/tree/master/oauth2_provider/tests


class TestOauth2Authentication(BaseTest):
    def test_is_token_valid(self):
        """ Test that the access token is valid """
        self.assertTrue(is_access_token_valid(self.token))

    def test_token_encryption(self):
        """ Test the encryption and decryption of the access token """
        enc_token = encrypt_access_token(self.token)

        self.assertTrue(enc_token)

        token = decrypt_access_token(enc_token)
        self.assertTrue(is_access_token_valid(token))
        self.assertTrue(token)

    def test_token_refresh(self):
        """ Test we can refresh the access token """
        self.assertTrue(refresh_access_token(self.token))

    def test_login_view(self):
        """
        Test the apps.accounts.views.sdLogin view. Post takes a username and password, returns a json response
        with the encrypted oauth2 token in a cookie named 'token'.
        """

        data = {
            'username': ADMIN_ACCOUNT_NAME,
            'password': ADMIN_ACCOUNT_PASSWORD,
        }

        url = reverse(login_view)

        # Test successful login
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.cookies)
        self.assertTrue(response.json()['status'] == 'OK')

        # Test bad login
        data = {
            'username': 'charles',
            'password': 'abc123',
        }

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['status'] == 'ERROR')

