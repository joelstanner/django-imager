from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class ImagerProfile(models.Model):

    user = models.OneToOneField(User)

    picture = models.ImageField()
    phone = models.CharField(max_length=20)
    birthday = models.DateField()

    name_priv = models.BooleanField(default=True)
    email_priv = models.BooleanField(default=True)
    picture_priv = models.BooleanField(default=True)
    phone_priv = models.BooleanField(default=True)
    birthday_priv = models.BooleanField(default=True)

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


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ImagerProfile.objects.create(
            birthday='1970-01-01', 
            picture='text.txt',
            phone='555-555-5555',
            user=instance)

post_save.connect(create_user_profile, sender=User)
