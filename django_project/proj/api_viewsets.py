#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#
from collections import OrderedDict

from rest_framework.decorators import action
from rest_framework.response import Response

from proj.models import RecordCount
from proj.serializer import *


class ModelViewSetWithCount(viewsets.ModelViewSet):
    """
    Extend the ModelViewSet with a count option
    """
    queryset = None

    # Return the Node model record count
    @action(detail=False)
    def count(self, request):
        try:
            count = RecordCount(self.queryset.count())  # Models
        except TypeError:
            count = RecordCount(len(self.queryset))  # Dict

        serializer = RecordCountSerializer(count)
        return Response(serializer.data)


class ReadOnlyModelViewSetWithCount(viewsets.ReadOnlyModelViewSet):
    """
    Extend the ReadOnlyModelViewSet with a count option
    """
    queryset = None

    # Return the Node model record count
    @action(detail=False)
    def count(self, request, count=None):
        try:
            if count is not None:
                count = RecordCount(count)
            else:
                count = RecordCount(self.queryset.count())  # Models
        except TypeError:
            count = RecordCount(len(self.queryset))  # Dict

        serializer = RecordCountSerializer(count)
        return Response(serializer.data)


class ReadOnlyModelViewSetWithCountModified(ReadOnlyModelViewSetWithCount):
    """
    Extend the ReadOnlyModelViewSetWithCount with a modified date option
    """
    queryset = None

    @action(detail=False)
    def modified(self, request, queryset=None, fields=None):

        items = []

        try:

            # If queryset is None, then return the full record set
            if queryset is None:
                fields = build_model_modified_field_list(self.queryset)
                queryset = self.queryset.values_list(*fields)
            else:
                fields = build_model_modified_field_list(queryset)

            # syncing relies on having Foreign Key values in output
            for item in queryset:
                # values = {'id': item[0], 'modified': item[1]}
                values = OrderedDict()
                cnt = 0
                for field in fields:
                    values[field] = item[cnt]
                    cnt += 1

                items.append(values)
        except Exception as e:
            pass

        serializer = ModifiedSerializer(items, many=True)
        return Response(serializer.data)


class ChooserListKeyBaseViewSet(ReadOnlyModelViewSetWithCount):
    """
    Generic ViewSet for Chooser Tuples
    """
    serializer_class = ChooserListKeyBaseSerializer
    queryset = []

    def __init__(self, data, resource_name, **kwargs):

        self.resource_name = resource_name
        self.queryset = []

        for (key, value) in data:
            self.queryset.append(ChooserList(len(self.queryset) + 1, key, value))

    def retrieve(self, request, *args, **kwargs):

        serializer = None

        if kwargs['pk']:
            key = kwargs['pk']

            # See if we need to convert key to int
            if self.queryset and isinstance(self.queryset[0].key, int):
                key = int(key)

            for item in self.queryset:
                if item.key == key:
                    serializer = self.serializer_class(item)
                    break

        if not serializer:
            instance = self.get_object()  # Will raise exception when there is no match

        return Response(serializer.data)


class ChooserListIDBaseViewSet(ChooserListKeyBaseViewSet):
    """
    Same as ChooseListKeyBaseViewSet with ID instead of Key identifier field
    """
    serializer_class = ChooserListIDBaseSerializer


def build_model_modified_field_list(queryset):
    """ Setup the field list for a 'modified' api query, add any Foreign Key field names """

    fields = list()
    fields.append('id')
    fields.append('modified')

    if not queryset:
        return fields

    try:
        for field in queryset.model._meta.local_fields:
            if field.is_relation:
                fields.append(field.name)
    except:
        pass

    return fields