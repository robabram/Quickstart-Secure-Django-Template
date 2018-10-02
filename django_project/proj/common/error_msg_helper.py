#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

from django.utils.translation import ugettext_lazy as _


def bootstrap_alert_message(msg, alert_type):
    """
    Wrap Ajax error message for display
    :param msg: Message text
    :param alert_type: must be alert-danger, alert-success, alert-info, alert-warning
    :return: html formatted message
    """

    if not msg:
        msg = _('An unknown error has occurred')

    if alert_type == 'error':
        alert_type = 'danger'

    if not alert_type or alert_type not in 'danger, success, info, warning':
        alert_type = 'warning'

    alert_label = alert_type
    if alert_label == 'danger':
        alert_label = 'error'

    f_msg = """
        <div class="alert alert-{0} alert-dismissable fade show">
          <button type="button" class="close" data-dismiss="alert">&times;</button>
          <strong>{1}:</strong> {2}.
        </div>
    """.format(alert_type, alert_label.title(), msg)

    return f_msg