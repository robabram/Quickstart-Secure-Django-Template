#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

import datetime
import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


@login_required
@require_http_methods(["GET"])
def overview(request):

    context = {}

    return render(request, 'dashboard/overview.html', context)


# @login_required
# @require_http_methods(["POST"])
# def ajax_get_update_status(request):
#
#     latest, update_ver = get_version_update_info()
#     response = 'Unable to get update information'
#
#     if update_ver is not None:
#
#         if 'error' not in update_ver:
#
#             if latest:
#                 response = '<span class="success" style="font-size: 14px;"><i class="fa fa-check-circle"> </i> {0}.</span>'.format(_('This system is on the latest version'))
#             else:
#                 response = 'Latest: {0} &nbsp;&nbsp;<a href="/system/update/">{1}</a>'.format(update_ver, _('Update Now'))
#         else:
#             return JsonResponse(dict([('status', 'error'), ('response',
#                                                             _('Unable to get update info, please check DNS settings')), ]))
#
#     return JsonResponse(dict([('status', 'OK'), ('response', response), ]))
