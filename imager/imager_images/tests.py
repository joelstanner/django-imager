from django.test import TestCase
from profiles.models import ImagerProfile
from django.contrib.auth.models import User
import factory


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ImagerProfile

    username = 'Bob'
