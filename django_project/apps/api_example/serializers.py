#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

from rest_framework import serializers
from apps.api_example.models import Temps


class TempsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temps
        exclude = ()
