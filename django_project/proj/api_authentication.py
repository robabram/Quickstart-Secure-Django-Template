#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

#
# Support for alternate authentication handling for Rest API calls
#
import logging

from proj.common.oauth_helper import decrypt_access_token, is_access_token_valid, get_user_from_token

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from oauth2_provider.models import AccessToken
from rest_framework import authentication, permissions
from rest_framework import exceptions

from django.core.exceptions import ObjectDoesNotExist

from apps.accounts.models import UserProfile

logger = logging.getLogger(__name__)


class APIAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        """
        security is handled by the Oauth2 rest framework authentication provider.
        Otherwise an API authentication header needs to be provided.
        """
        # TODO: Remove this later after all auth headers have been coded for.
        # return None

        # Try Oauth2 authentication first
        if 'token' in request.COOKIES:

            # Get the encrypted access token data, fix any equal sign encoding.
            enc_token = request.COOKIES['token'].replace('%3D', '=').encode('UTF-8')
            token = decrypt_access_token(enc_token)

            # Add the HTTP_Authorization header based off the encrypted token.
            # We can only add something to the META property if we make a copy and store back the copy.
            meta = request.META.copy()
            meta['HTTP_Authorization'] = 'bearer {0}'.format(token['access_token'])
            request.META = meta

            # Retrieve the AccessToken record from the DB.
            request.auth = AccessToken.objects.get(token=token['access_token'])

            result = OAuth2Authentication().authenticate(request)
            return result

        # Try API_KEY authentication
        if "HTTP_API_KEY" in request.META:
            m_key = request.META.get('HTTP_API_KEY')

            # Look up API key in UserProfile table.
            try:
                profile = UserProfile.objects.get(api_code=m_key)

                if profile.user.is_active is True and profile.api_access is True:
                    return (profile.user, m_key)

            except ObjectDoesNotExist:
                pass

        raise exceptions.AuthenticationFailed('Valid API credentials were not provided.')

    def has_permission(self, request, view):
        """
        Validate user has permission for the view
        """

        if 'HTTP_API_KEY' in request.META or'token' in request.COOKIES:
            return True

        return False

    def has_object_permission(self, request, view, obj):

        # Always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # If needed, decide if access to view and obj are allowed.
        # http://www.django-rest-framework.org/api-guide/permissions/#examples
        return True
