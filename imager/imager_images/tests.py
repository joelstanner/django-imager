from __future__ import print_function
from django.test import TestCase
from profiles.models import ImagerProfile
from django.contrib.auth.models import User
import factory


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'Bob'


class TestPhoto(TestCase):

    def setUp(self):
        self.user1 = UserFactory.create()
        self.user2 = UserFactory.create(username='alice')

    def test_Photo_saves_a_picture(self):
        
