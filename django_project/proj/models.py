#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.fields.related import ManyToManyField

import logging
logger = logging.getLogger(__name__)


class ChooserList(object):
    """
    Serialization Object for tuple lists.
    """
    def __init__(self, pk, key, value):
        self.pk = pk
        self.id = self.key = key
        self.value = self.descr = value


class RecordCount (object):
    """
    Generic record count class, used for serialization of record counts
    """
    def __init__(self, count):
        self.data = {'count': count}


class ModifiedList (object):
    """ Used by API to return only the id and modified date for model records """
    def __init__(self, rec_id, modified):
        self.id = rec_id
        self.modified = modified


class BaseModel(models.Model):
    """
    Add a default 'created' and 'modified' field.
    Allow exporting record field data to a dictionary object.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    # https://stackoverflow.com/questions/21925671/convert-django-model-object-to-dict-with-all-of-the-fields-intact
    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        opts = self._meta
        data = {}
        for f in opts.concrete_fields + opts.many_to_many:
            if isinstance(f, ManyToManyField):
                if self.pk is None:
                    data[f.name] = []
                else:
                    data[f.name] = list(f.value_from_object(self).values_list('pk', flat=True))
            else:
                data[f.name] = f.value_from_object(self)
        return data


def get_client_ip(request):

    if request is None:
        return ''

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


#
# Handle login signals, a good place to log user activity
#
def sig_user_logged_in(sender, user, request, **kwargs):
    """
    A user has logged in
    """
    pass


def sig_user_logged_out(sender, user, request, **kwargs):
    """
    A user has logged out
    """
    pass


def sig_user_login_failed(sender, **kwargs):
    """
    # Using django-axes to manage lockout after failed attempts.
    # This is just to log the event in our web_log table.
    """



    uname = kwargs['credentials']['username']

    # Try to match up with an existing user record
    try:
        user = User.objects.get(username=uname)
    except User.DoesNotExist:
        # activity_logger(-1, 'LOGIN_FAIL', content='user: unknown')
        pass
    else:
        # activity_logger(user.id, 'LOGIN_FAIL', content='user:%s' % (uname))
        pass

#
# Connect signals to functions
#
user_logged_in.connect(sig_user_logged_in)
user_logged_out.connect(sig_user_logged_out)
user_login_failed.connect(sig_user_login_failed)
