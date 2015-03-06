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

    imagerprofile = UserFactory.create().ImagerProfile


class TestPhoto(TestCase):

    def setUp(self):
        self.user1 = UserFactory.create()
        self.user2 = UserFactory.create(username='Alice')

    @unittest.skip("don't test")
    def test_Photo_saves_a_picture(self):
        self.user1.photo
        pass

    def test_create_a_new_photo_file(self):
        photo1 = PhotoFactory.create()
