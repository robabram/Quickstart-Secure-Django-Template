#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

from proj.api_viewsets import ReadOnlyModelViewSetWithCountModified
from apps.api_example.models import Temps
from apps.api_example.serializers import TempsSerializer


class TempsViewSet(ReadOnlyModelViewSetWithCountModified):
    """
    Example API Model View Set - Read Only.

    API's included with the ReadOnlyModelViewSetWithCountModified base ViewSet:

    1) '/api/api_example/temps/' - This is the base api that returns all detail.
    2) '/api/api_example/temps/count/' - Returns the record count.
    3) '/api/api_example/temps/modified/' - Returns only the PK and modified fields.
    4) '/api/api_example/temps/{id}/' - Returns the record matching the given ID value.

    """
    queryset = Temps.objects.all()
    serializer_class = TempsSerializer