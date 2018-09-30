#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#

#
# Some enhanced API serializers to enhance things.
# User and User Profile serializers.
#


import json
from django.core import serializers as core_serializer
from rest_framework import serializers, viewsets, mixins
from django.contrib.auth.models import User, Group
from apps.accounts.models import UserProfile
from proj.models import ChooserList


class ChooserListKeyBaseSerializer(serializers.Serializer):
    """
    Generic Serializer for Chooser Tuples
    """
    key = serializers.CharField(max_length=50)
    value = serializers.CharField(max_length=100)


class ChooserListIDBaseSerializer(serializers.Serializer):
    """
    Generic Serializer for Chooser Tuples
    """
    id = serializers.IntegerField()
    descr = serializers.CharField(max_length=100)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('accepted_terms', 'email_reg_code', 'account_activated', 'oauth_scope')


class UserSerializer(serializers.ModelSerializer):
    # profile = UserProfileSerializer(many=False)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_superuser')


class UserNameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class RecordCountSerializer(serializers.Serializer):
    count = serializers.ReadOnlyField()

    def to_representation(self, instance):
        return {
            'count': instance.data['count'],
        }


class ModifiedSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    modified = serializers.DateTimeField()

    # If our instance has extra fields, add them to the output
    def to_representation(self, instance):
        ret = super(ModifiedSerializer, self).to_representation(instance)

        for key, val in instance.items():
            if key not in ret:
                ret[key] = val
        return ret


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')



