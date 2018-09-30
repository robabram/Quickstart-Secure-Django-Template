#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

#
# https://blndxp.wordpress.com/2016/03/04/django-get-current-user-anywhere-in-your-code-using-a-middleware/
#

from threading import local

from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from proj.common.oauth_helper import encrypt_access_token, decrypt_access_token
from proj.common.oauth_helper import is_access_token_valid, refresh_access_token

_thread_locals = local()


def get_current_request():
    """ returns the request object for this thread """
    return getattr(_thread_locals, "request", None)


def get_current_user():
    """ returns the current user, if exist, otherwise returns None """
    request = get_current_request()
    if request:
        return getattr(request, "user", None)


class ThreadLocalMiddleware:
    """
    Simple middleware that adds the request object in thread local storage.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.

        _thread_locals.request = request

        response = self.get_response(request)

        # Code to be executed for each request/response after the view is called.

        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request

        return response


class OAuthTokenCookieMiddleware(MiddlewareMixin):
    """
    Authenticate this request by decrypting the Oauth token and validating it.
    We also refresh the token if needed as well.
    """

    def process_request(self, request):

        # Check to see if this is the login/logout page, if so just return.
        if '/accounts/login/' in request.path or '/accounts/logout/' in request.path:
            return

        if 'token' in request.COOKIES:

            # Get the encrypted access token data, fix any equal sign encoding.
            enc = request.COOKIES['token'].replace('%3D', '=').encode('UTF-8')

            # Decrypt the access token data
            token = decrypt_access_token(enc)

            # Check for a valid oauth token.
            if token is not None and 'access_token' in token:

                # Check to see if access token is not valid.
                if not is_access_token_valid(token):

                    # TODO: Figure out when we should *not* just refresh the token.
                    # Try to refresh the token.
                    token = refresh_access_token(token)

                    # If we have a good refreshed token, update the cookies.
                    if 'access_token' in token:

                        # Encrypt the new token
                        enc = encrypt_access_token(token)

                        # Set the token into the request object
                        cookies = request.COOKIES.copy()
                        cookies['token'] = enc.decode('UTF-8')
                        cookies['token-update'] = "1"

                        request.COOKIES = cookies.copy()

                    else:
                        # Refresh token failed
                        return HttpResponseRedirect('/accounts/logout/')

                # Create the Authorization header with the access token.
                request.META['Authorization'] = 'bearer {0}'.format(token['access_token'])

        else:
            pass

    def process_response(self, request, response):

        # If the request object has an 'token-update' cookie, update the token cookie from the request object.
        if 'token-update' in request.COOKIES:
            response.set_cookie('token', request.COOKIES['token'])

        return response
