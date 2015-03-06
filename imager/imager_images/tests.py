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


class AlbumFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Album

    user = UserFactory.create(username='Freddy')


class TestPhoto(TestCase):

    def setUp(self):
        self.user1 = UserFactory.create()
        self.user2 = UserFactory.create(username='Alice')
        self.photo1 = PhotoFactory.create(profile=self.user1.ImagerProfile)
        self.photo2 = PhotoFactory.create(profile=self.user2.ImagerProfile)

    def test_create_a_new_photo_file(self):
        self.assertEqual(self.photo1.profile.user.username, 'Bob')
        self.assertEqual(self.photo1.title, 'No Title')
        self.assertEqual(self.photo1.description, 'No Description')
        self.assertEqual(self.photo1.published, 'pv')

    def test_photo_belongs_to_unique_user(self):
        self.assertEqual(str(self.photo1.profile), 'Bob')


class TestAlbum(TestCase):

    def setUp(self):
        self.user1 = UserFactory.create()
        self.user2 = UserFactory.create(username='Alice')
        self.photo1 = PhotoFactory.create(profile=self.user1.ImagerProfile)
        self.photo2 = PhotoFactory.create(profile=self.user2.ImagerProfile)
        self.album1 = AlbumFactory.create()
        self.bobalbum = AlbumFactory.create(user=self.user1)

    #def test_album_has_a_user(self):
    #    self.assertEqual
    
    def test_new_album_is_empty(self):
        pass
    
    def test_album_attributes(self):
        pass
    
    def test_album_add_a_photo(self):
        pass
    
    def test_album_designate_cover(self):
        pass
    
    def test_album_photos_only_from_album_user(self):
        pass
    
    
        
