from django.conf import settings
from django.db import models

class Dismissed(models.Model):
    """
    The existence of a dismissed object indicates that a user has seen and
    dismissed the corresponding hint.

    """

    key = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        unique_together = ('key', 'user',)
