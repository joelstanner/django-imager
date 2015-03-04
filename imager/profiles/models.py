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

    follows = models.ManyToManyField("self", symmetrical=False)

    blocked = models.ManyToManyField("self")

    def block(self, IProfile):
        if IProfile in self.blocked.all():
            raise ValueError('You been BLOCKED!')
        self.blocked.add(IProfile)
        pass

    def following(self):
        follow_list = self.follows.all()
        for follow in follow_list:
            if follow in self.blocked.all():
                follow.delete()
        return follow_list

    def followers(self):
        followed_by_list = self.imagerprofile_set.all()
        for follow in followed_by_list:
            if follow in self.blocked.all():
                follow.delete()
        return followed_by_list

    def follow(self, IProfile):
        if IProfile in self.blocked.all():
            raise ValueError('You been BLOCKED!')
        self.follows.add(IProfile)

    def unfollow(self, IProfile):
        if IProfile in self.blocked.all():
            raise ValueError('You been BLOCKED!')
        if type(IProfile) is not type(self):
            raise ValueError()
        self.follows.remove(IProfile)

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


# class Following(models.Model):
#     """Who's following who"""
#     following = models.ForeignKey(ImagerProfile)
#     followed = models.ForeignKey(ImagerProfile)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ImagerProfile.objects.create(
            birthday='1970-01-01',
            picture='text.txt',
            phone='555-555-5555',
            user=instance)

post_save.connect(create_user_profile, sender=User)
