#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

import unittest
from unittest import TestCase
from oauth2_provider.settings import oauth2_settings
from proj.common.oauth_helper import encrypt_access_token, decrypt_access_token


# Test the AESCipher encrypt and decrypt methods
class TestCryptoData(TestCase):

    def test_oauth_crypto(self):

        phrase = 'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE'

        token = {
            'access_token': 'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE',
            'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
            'token_type': 'Password',
            'refresh_token': 'abc',
            'scope': 'read write'
        }

        data = encrypt_access_token(token)

        if not data:
            self.fail()

        result = decrypt_access_token(data)

        if not result:
            self.fail()

        if phrase != result['access_token']:
            self.fail('Decrypted value does not match phrase.')


if __name__ == '__main__':
    unittest.main()
