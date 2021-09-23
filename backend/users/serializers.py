""" User's serializers. """

from rest_framework import serializers
from .models.user import User

class UserTokenSerializer(serializers.ModelSerializer):
    """ User token serializer. """

    class Meta:
        """ Meta class. """
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')