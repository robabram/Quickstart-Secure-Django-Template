#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.translation import ugettext_lazy as _

from proj.common.error_msg_helper import bootstrap_alert_message

register = template.Library()


@register.filter
@stringfilter
def form_message(value):

    if not value:
        return ''

    try:
        msg_type, message = value.split('|')
    except ValueError:
        return '<div class="alert alert-error clearfix"> Invalid form message passed. Debug Me! </div>'

    if msg_type == 'error':
        msg_type = 'danger'

    # Type must be one of 'success', 'info', 'warning' or 'danger'.
    return bootstrap_alert_message(message, msg_type)


register.filter('form_messages', form_message)

