
from annoying import fields as annoying_fields 

from django.db import models


class CCCBProfile(models.Model):
    """The CCCB Member Profile"""
    member = annoying_fields.AutoOneToOneField(
        to='members.Member',
        on_delete=models.CASCADE,
        related_name='cccb_profile')

    is_keyholder = models.BooleanField(default=False)

