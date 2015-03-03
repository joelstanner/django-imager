from django.db import models
from django.contrib.auth.models import User


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
        pass
