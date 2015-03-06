from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

import datetime


@python_2_unicode_compatible
class Photo(models.Model):
    '''Represent an individual photo'''

    profile = models.ForeignKey('profiles.ImagerProfile')

    photo = models.ImageField(blank=True)

    def __str__(self):
        return self.pk


@python_2_unicode_compatible
class Album(models.Model):
    '''Represent an individual album of photos'''

    def __str__(self):
        return self.pk
