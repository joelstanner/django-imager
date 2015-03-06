from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

import datetime


@python_2_unicode_compatible
class Album(models.Model):
    '''Represent an individual album of photos'''

    user = models.ForeignKey(User, related_name='album_set')
    photos = models.ManyToManyField('Photo', symmetrical=False, related_name='album_set')

    title = models.CharField(max_length=200, default='No Title')
    description = models.TextField(default='No Description')

    cover = models.ImageField(blank=True, null=True)

    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(null=True)

    PUBLIC = 'pb'
    PRIVATE = 'pv'
    SHARED = 'sh'

    PUBLISHED_CHOICES = (
        (PUBLIC, 'public'),
        (PRIVATE, 'private'),
        (SHARED, 'shared')
    )

    published = models.CharField(max_length=2,
                                 choices=PUBLISHED_CHOICES, default='pv')

    def add_photo(self, photo):
        if photo.profile.user != self.user:
            raise AttributeError()
        self.photos.add(photo)

    def designate_cover(self, photo):
        self.cover = photo.photo

    def __str__(self):
        return self.pk


@python_2_unicode_compatible
class Photo(models.Model):
    '''Represent an individual photo'''

    PUBLIC = 'pb'
    PRIVATE = 'pv'
    SHARED = 'sh'

    PUBLISHED_CHOICES = (
        (PUBLIC, 'public'),
        (PRIVATE, 'private'),
        (SHARED, 'shared')
    )

    profile = models.ForeignKey('profiles.ImagerProfile', related_name='photo_set')

    album = models.ManyToManyField(Album, related_name='photo_set',
                                   null=True, blank=True)

    photo = models.ImageField(blank=True, null=True)

    title = models.CharField(max_length=200, default='No Title')
    description = models.TextField(default='No Description')

    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(null=True)

    published = models.CharField(max_length=2,
                                 choices=PUBLISHED_CHOICES, default='pv')

    def __str__(self):
        return self.title
