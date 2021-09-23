""" Django models utilities """

# Django
from django.db import models

class CompeWodModel(models.Model):
    """ CompeWod base model.
    CompeWodModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
        + created (DateTime): Stores the datetime object was created
        + modified (DateTime): Stores the datetime object was modified
    """
    created = models.DateTimeField(
        'created_at',
        auto_now_add=True,
        help_text='Date time on which the object was created.'
    )

    modified = models.DateTimeField(
        'modified_at',
        auto_now=True,
        help_text='Date time on which the object was last modified.'
    )

    class Meta():
        """Meta options"""

        abstract=True

        get_latest_by = 'created'
        ordering = ['-created', '-modified']



