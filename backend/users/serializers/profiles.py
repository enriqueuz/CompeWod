""" Profiles serializers. """

# REST Framework
from rest_framework import serializers

# Models
from ..models.profiles import Profile
from ..models.users import User

class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""

    first_name = serializers.CharField(
        min_length=2, 
        max_length=30, 
        write_only=True
        )
    last_name = serializers.CharField(
        min_length=2, 
        max_length=30, 
        write_only=True
        )
    phone_number = serializers.CharField(
        validators=[User.phone_regex],
        write_only=True
        )

    class Meta:
        """Meta class."""

        model = Profile
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'picture',
            'biography',
            'birth_date', # TODO: This should only be changeable a few times
            'sex', # This too
            'type',
            'weight',
            'height'

        )

    def validate_weight(self, value):
        """ Check that weight is not over 700 kg. """
        # NOTE: I am not sure of this validation, heviest person's weight ever
        # was 635 kg so this kinda makes sense to me, but not sure.

        if value > 700:
            raise serializers.ValidationError(
                'Weight is over 700 kg, are you sure it is right?'
                )
        
        return value
    
    def validate_height(self, value):
        """ Check that height is not over 280 cm. """
        # NOTE: Same as in height

        if value > 280:
            raise serializers.ValidationError(
                'Height is over 280 cm, are you sure it is right?'
                )
        
        if value < 50:
            raise serializers.ValidationError(
                'Height is under 50 cm, are you sure it is right?'
                )
        
        return value
    
    def save(self):
        """ Save names and phone numbers to User. """
        super(ProfileModelSerializer, self).save()
        
        user = self.instance.user
        
        if 'first_name' in self.validated_data: 
            first_name = self.validated_data['first_name']
            user.first_name = first_name
        
        if 'last_name' in self.validated_data:
            last_name = self.validated_data['last_name']
            user.last_name = last_name

        if 'phone_number' in self.validated_data: 
            phone_number = self.validated_data['phone_number']
            user.phone_number = phone_number

        # TODO: Maybe find a better way? I just don't want to save instance if
        # it is not necessary.
        if ('first_name' in self.validated_data or 
            'last_name' in self.validated_data or 
            'phone_number' in self.validated_data):
            user.save()

 

