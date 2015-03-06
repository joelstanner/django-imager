from __future__ import print_function
from django.test import TestCase
import unittest
from profiles.models import ImagerProfile
from django.contrib.auth.models import User
from models import Photo, Album
import factory


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'Bob'


class PhotoFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Photo

    profile = UserFactory.create(username='Bobby').ImagerProfile


class TestPhoto(TestCase):

    def setUp(self):
        self.user1 = UserFactory.create()
        self.user2 = UserFactory.create(username='Alice')

    def test_create_a_new_photo_file(self):
        photo1 = PhotoFactory.create()
        self.assertEquals(photo1.profile.user.username, 'Bobby')
        self.assertEquals(photo1.title, 'No Title')
        self.assertEquals(photo1.description, 'No Description')
        self.assertEquals(photo1.published, 'pv')

