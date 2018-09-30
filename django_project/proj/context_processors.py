#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

import re
from django.urls import resolve


def user_can_edit(request):
    """ Is the user allowed to edit? Query Oauth scopes to verify. """

    can_edit = False

    try:
        can_edit = 'write' in request.user.profile.oauth_scope

        mode_pattern = '^.*?/(?P<mode>(view|edit))/$'
        match = re.match(mode_pattern, request.path)

        if match:
            can_edit = True if match.group('mode') == 'edit' and 'write' in request.user.profile.oauth_scope else False

    except Exception:
        pass

    # return False  # Debug only
    return can_edit


def can_edit_processor(request):
    """ decide if the user can edit or not """

    can_edit = user_can_edit(request)

    return {'can_edit': can_edit}

