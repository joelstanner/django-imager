from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    is_active = True

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    picture = models.FileField(max_length=255)
    phone = models.CharField(max_length=20)
    birthday = models.DateField()

    name_piv = models.BooleanField(default=True)
    email_piv = models.BooleanField(default=True)
    picture_piv = models.BooleanField(default=True)
    phone_piv = models.BooleanField(default=True)
    birthday_piv = models.BooleanField(default=True)
