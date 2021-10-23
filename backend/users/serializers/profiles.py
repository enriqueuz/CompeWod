""" Profiles serializers. """

# REST Framework
from rest_framework import serializers

# Models
from ..models.profiles import Profile

class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""

    class Meta:
        """Meta class."""

        model = Profile
        fields = (
            'picture',
            'biography',

        )
        read_only_fields = (
            'rides_taken',
            'rides_offered',
            'reputation'
        )