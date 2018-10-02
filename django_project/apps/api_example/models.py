#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#


from django.db import models
from django.utils.translation import ugettext_lazy as _

from proj.models import BaseModel


class Temps(BaseModel):
    """
    BaseModel includes Created and Modified date fields
    """

    id = models.IntegerField(primary_key=True)
    date = models.DateField(_('Date'))
    new_york = models.FloatField(_('New York'))
    san_francisco = models.FloatField(_('San Francisco'))
    austin = models.FloatField(_('Austin'))

    class Meta:
        db_table = 'example_temps'
