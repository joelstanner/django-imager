from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

import datetime


@python_2_unicode_compatible
class ImagerProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    picture = models.ImageField(blank=True)
    phone = models.CharField(max_length=20, default='No Phone')
    birthday = models.DateField(default=datetime.date.today)

    name_priv = models.BooleanField(default=True)
    email_priv = models.BooleanField(default=True)
    picture_priv = models.BooleanField(default=True)
    phone_priv = models.BooleanField(default=True)
    birthday_priv = models.BooleanField(default=True)

    followers = models.ManyToManyField(User, through='Following')

    def followers(self):
        pass

    def __str__(self):
        return self.user.username

    def is_active(self):
        return self.user.is_active

    @classmethod
    def active(cls):
        active_users = []
        profiles = ImagerProfile.objects.all()
        for prof in profiles:
            if prof.user.is_active is True:
                active_users.append(prof)
        return active_users


class Following(models.Model):
    """Who's following who"""

    following = models.ForeignKey(ImagerProfile)
    followed = models.ForeignKey(ImagerProfile)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ImagerProfile.objects.create(
            birthday='1970-01-01',
            picture='text.txt',
            phone='555-555-5555',
            user=instance)

post_save.connect(create_user_profile, sender=User)
