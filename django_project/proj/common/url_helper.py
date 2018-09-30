#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

#
# A simple helper for building urls with parameters when using Reverse()
#

from urllib import parse
from django.urls import reverse


def build_url(*args, **kwargs):
    """
    http://stackoverflow.com/questions/9585491/how-do-i-pass-get-parameters-using-django-urlresolvers-reverse
    """
    get = kwargs.pop('get', {})
    url_str = reverse(*args, **kwargs)

    if get:
        url_str += '?' + parse.urlencode(get)

    return url_str