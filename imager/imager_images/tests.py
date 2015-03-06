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
        self.photo1 = PhotoFactory.create(profile=self.user1.ImagerProfile)
        self.photo2 = PhotoFactory.create(profile=self.user2.ImagerProfile)

    def test_create_a_new_photo_file(self):
        self.assertEquals(self.photo1.profile.user.username, 'Bob')
        self.assertEquals(self.photo1.title, 'No Title')
        self.assertEquals(self.photo1.description, 'No Description')
        self.assertEquals(self.photo1.published, 'pv')

    #def test_photo_belongs_to_unique_user(self):
    #    pass
