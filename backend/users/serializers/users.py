""" User's serializers. """

# Django
from django.contrib.auth import password_validation

# REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Models
from ..models.users import User
from ..models.profiles import Profile

# Serializers
from .profiles import ProfileModelSerializer

class UserTokenSerializer(serializers.ModelSerializer):
    """ User token serializer. """

    class Meta:
        """ Meta class. """
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfileModelSerializer()

    class Meta:
        """Meta class."""

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile'
        )

class UserReadOnlyModelSerializer(UserModelSerializer):

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        read_only_fields = '__all__'


class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer.
    Handle sign up data validation and user/profile creation.
    """

    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), 
                message='A user with this email already exists'
                )
            ]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), 
                message='A user with this username already exists'
                )
            ]
    )

    # Phone number
    phone_number = serializers.CharField(validators=[User.phone_regex])

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, data):
        """Verify passwords match."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Handle user and profile creation."""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified=False, is_client=True)
        Profile.objects.create(user=user)
        return user
