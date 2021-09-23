""" Users app models. """

# Django
from django.core import validators
from django.core.validators import RegexValidator
from django.db import models

# Models
from utils.models import CompeWodModel
from django.contrib.auth.models import AbstractUser

class User(CompeWodModel, AbstractUser):
    """ User model.
    
        Extend from Django's Abstract User, change the username field
        to email and add some extra fields.
    """

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email address already exists'
        }
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message=("Phone number must be entered in the format: +123456789. "
            "Up to 15 digits allowed")
    )

    phone_number = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

    is_client = models.BooleanField(
        'client status',
        default=True,
        help_text=(
            'Help easily distinguish users and perform queries.'
            'Clients are the main type of user'
        )
    )

    is_verified = models.BooleanField(
        'verified',
        default=False                                                                                                                                                                                                                                                                               ,
        help_text='Set to true when the user have verfied its email address'
    )

    def __str__(self):
        """ Return username. """
        return self.username
    
    def get_short_name(self):
        """ Return username. """
        return self.username