#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

import random
import string

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from timezone_field import TimeZoneFormField

# Add the user profile to the django.contrib.auth.models.User object and
# auto create the user profile database record if it does not exist
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

ROLE_CHOICES = (
    ('read write', _('Read/Write')),
    ('read', _('Read Only')),
)

PAGE_SIZE_CHOICES = (
    (10, '10'),
    (15, '15'),
    (20, '20'),
    (25, '25'),
    (50, '50'),
    (75, '75'),
    (100, '100'),
    (250, '250'),
    (500, '500'),
    (1000, '1000'),
)

UTC_OFFSETS = [("-14:00", "-14:00"), ("-13:00", "-13:00"), ("-12:00", "-12:00"), ("-11:00", "-11:00"),
               ("-10:00", "-10:00"), ("-09.30", "-09.30"), ("-09:00", "-09:00"), ("-08:00", "-08:00"),
               ("-07:00", "-07:00"), ("-06:00", "-06:00"), ("-05:00", "-05:00"), ("-04:00", "-04:00"),
               ("-03:00", "-03:00"), ("-02:00", "-02:00"), ("-01:00", "-01:00"), ("+00:00", "+00:00"),
               ("+01:00", "+01:00"), ("+02:00", "+02:00"), ("+03:00", "+03:00"), ("+03:30", "+03:30"),
               ("+04:00", "+04:00"), ("+04:30", "+04:30"), ("+05:00", "+05:00"), ("+05.30", "+05.30"),
               ("+05:45", "+05:45"), ("+06:00", "+06:00"), ("+07:00", "+07:00"), ("+08:00", "+08:00"),
               ("+08:30", "+08:30"), ("+08:45", "+08:45"), ("+09:00", "+09:00"), ("+09:30", "+09:30"),
               ("+10:00", "+10:00"), ("+10:30", "+10:30"), ("+11:00", "+11:00"), ("+12:00", "+12:00"),
               ("+12:45", "+12:45"), ]

def generate_api_code():
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits + '$!^') for _ in range(35))


class UserProfile(models.Model):
    """
    UserProfile gets attached the User database object. IE: User.profile.url
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    accepted_terms = models.BooleanField(default=False)
    email_reg_code = models.CharField(max_length=25, db_index=True)
    account_activated = models.BooleanField(default=False)
    oauth_scope = models.CharField(max_length=255, choices=ROLE_CHOICES, default='read write') #'read write')
    timezone = models.CharField(_('Timezone'), max_length=256, default='America/Denver')
    page_size = models.IntegerField(_('Page Result Size'), default=20,
                                    validators=[MinValueValidator(0), MaxValueValidator(100), ])
    api_access = models.BooleanField(_('API Access'), default=False)
    api_code = models.CharField(_('API Auth Token'), max_length=35, default=None, null=True, blank=True)

    class Meta:
        db_table = 'auth_user_profile'
