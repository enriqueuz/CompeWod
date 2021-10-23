""" Profile model. """

# Django
from django.db import models

# Models
from utils.models import CompeWodModel

class Profile(CompeWodModel):
    """ Profile model.
    
        
    """

    user = models.OneToOneField(
        'users.User', 
        on_delete=models.CASCADE,
        related_name='profile'
        )
    picture = models.ImageField(
        'profile picture',
        upload_to='users/pictures/',
        blank=True,
        null=True
    )
    biography = models.TextField(max_length=500, blank=True)

    birth_date = models.DateField(null=True, blank=True)

    # TODO: Find later a solution in conjuction with the frontend to 
    # enter custom sex
    female = 'F'
    male = 'M'
    other = 'O'

    sex_options = [
        (female, 'Female'),
        (male, 'Male'),
        (other, 'Other')
    ]
    sex = models.CharField(choices=sex_options, max_length=6, blank=True)

    athlete = 'AT'
    judge = 'JU'
    box_owner = 'BO'

    type_choices = [
        (athlete, 'Athlete'),
        (judge, 'Judge'),
        (box_owner, 'Box owner')
    ]
    type = models.CharField(choices=type_choices, max_length=9, default=athlete)

    weight = models.FloatField(null=True, blank=True)

    height = models.FloatField(null=True, blank=True)

    # TODO: Foreign key to athlete's box
    box = None
    
    def __str__(self):
        """ Return username. """
        return self.user.username
    
    def get_short_name(self):
        """ Return username. """
        return self.user.username