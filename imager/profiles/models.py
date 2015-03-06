from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

import datetime


@python_2_unicode_compatible
class ImagerProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='ImagerProfile')
    picture = models.ImageField(blank=True)
    phone = models.CharField(max_length=20, default='No Phone')
    birthday = models.DateField(default=datetime.date.today)

    name_priv = models.BooleanField(default=True)
    email_priv = models.BooleanField(default=True)
    picture_priv = models.BooleanField(default=True)
    phone_priv = models.BooleanField(default=True)
    birthday_priv = models.BooleanField(default=True)

    follows = models.ManyToManyField("self",
                                     related_name='followers_set',
                                     symmetrical=False,
                                     blank=True)

    blocked = models.ManyToManyField("self",
                                     related_name='blockedby_set',
                                     symmetrical=False,
                                     blank=True)

    def blocked_by(self):
        return self.blockedby_set.all()

    def block(self, IProfile):
        if IProfile in self.blockedby_set.all():
            raise ValueError('You been BLOCKED!')
        self.blocked.add(IProfile)

    def unblock(self, IProfile):
        if IProfile not in self.blocked.all():
            raise ValueError('Not in blocked list')
        for block in self.blocked.all():
            if block == IProfile:
                self.blocked.remove(block)
                break

    def following(self):
        follow_list = self.follows.all()
        for follow in follow_list:
            if follow in self.blockedby_set.all():
                follow.delete()
        return follow_list

    def followers(self):
        followed_by_list = self.followers_set.all()
        for follow in followed_by_list:
            if follow in self.blockedby_set.all():
                follow.delete()
        return followed_by_list

    def follow(self, IProfile):
        if IProfile in self.blockedby_set.all():
            raise ValueError('You been BLOCKED!')
        self.follows.add(IProfile)

    def unfollow(self, IProfile):
        if IProfile in self.blockedby_set.all():
            raise ValueError('You been BLOCKED!')
        if type(IProfile) is not type(self):
            raise ValueError()
        self.follows.remove(IProfile)

    def add_album(self, album):
        if album.profile not in self.blockedby_set.all():
            if album.published == 'pb':
                self.profile.album_set.add(album)

    def is_active(self):
        return self.user.is_active


    def __str__(self):
        return self.user.username

    @classmethod
    def active(cls):
        active_users = []
        profiles = ImagerProfile.objects.all()
        for prof in profiles:
            if prof.user.is_active is True:
                active_users.append(prof)
        return active_users


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ImagerProfile.objects.create(
            birthday='1970-01-01',
            picture='text.txt',
            phone='555-555-5555',
            user=instance)

post_save.connect(create_user_profile, sender=User)
