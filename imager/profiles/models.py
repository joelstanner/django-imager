from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.db.models import Q
import datetime


class BlockedManager(models.Manager):
    def get_queryset(self):
        qs = super(BlockedManager, self).get_queryset()
        qs.get(blockedby_set__contains='Bob')


@python_2_unicode_compatible
class ImagerProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='ImagerProfile')
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

    objects = models.Manager()
    blockman = BlockedManager()

    def blocked_by(self):
        return self.blockedby_set.all()

    def block(self, IProfile):
        if IProfile in self.blockedby_set.all():
            raise ValueError('You been BLOCKED!')
        self.blocked.add(IProfile)

    def unblock(self, IProfile):
        if IProfile not in self.blocked.all():
            raise ValueError('Not in blocked list')
        self.blocked.remove(IProfile)

    def following(self):
        return self.follows.exclude(blocked=self)

    def followers(self):
        return self.followers_set.exclude(blocked=self)

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
        if album.profile in self.blockedby_set.all():
            raise ValueError('You been BLOCKED!')
        if album.published != 'pb':
            raise ValueError('This album is not public')
        self.album_set.add(album)

    def add_photo(self, photo):
        if photo.profile in self.blockedby_set.all():
            raise ValueError('You been BLOCKED!')
        if photo.published == 'pb':
            self.photo_set.add(photo)
        else:
            raise ValueError('This photo is not public')

    def show_photos(self):
        return self.photo_set.exclude(Q(profile__blocked=self) |
                                      Q(profile__blockedby_set=self))

    def show_albums(self):
        return self.album_set.exclude(Q(profile__blocked=self) |
                                      Q(profile__blockedby_set=self))

    def is_active(self):
        return self.user.is_active

    def __str__(self):
        return self.user.username

    @classmethod
    def active(cls):
        return ImagerProfile.objects.exclude(user__is_active=False)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ImagerProfile.objects.create(
            birthday='1970-01-01',
            picture='text.txt',
            phone='555-555-5555',
            user=instance)

post_save.connect(create_user_profile, sender=User)
