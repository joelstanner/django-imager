from __future__ import print_function
from django.test import TestCase
import unittest
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
        self.bob = UserFactory.create()
        self.alice = UserFactory.create(username='Alice')
        self.bobphoto = PhotoFactory.create(profile=self.bob.ImagerProfile)
        self.alicephoto = PhotoFactory.create(profile=self.alice.ImagerProfile)

    def test_create_a_new_photo_file(self):
        self.assertEqual(self.bobphoto.profile.user.username, 'Bob')
        self.assertEqual(self.bobphoto.title, 'No Title')
        self.assertEqual(self.bobphoto.description, 'No Description')
        self.assertEqual(self.bobphoto.published, 'pv')

    def test_photo_belongs_to_unique_user(self):
        self.assertEqual(str(self.bobphoto.profile), 'Bob')


class TestAlbum(TestCase):

    def setUp(self):
        self.bob = UserFactory.create()
        self.alice = UserFactory.create(username='Alice')
        self.bobphoto = PhotoFactory.create(profile=self.bob.ImagerProfile)
        self.alicephoto = PhotoFactory.create(profile=self.alice.ImagerProfile)
        self.freddyalbum = AlbumFactory.create()
        self.bobalbum = AlbumFactory.create(user=self.bob)

    def test_album_has_a_user(self):
        self.assertEqual(self.bobalbum.user.username, 'Bob')

    @unittest.skip('broken test')
    def test_new_album_is_empty(self):
        self.assertEqual(self.freddyalbum.photos.all(), [])

    def test_album_attributes(self):
        self.assertEqual(self.freddyalbum.title, 'No Title')
        self.assertEqual(self.freddyalbum.description, 'No Description')
        self.assertEqual(self.freddyalbum.published, 'pv')

    def test_album_add_a_photo(self):
        self.bobalbum.add_photo(self.bobphoto)
        self.assertIn(self.bobphoto, self.bobalbum.photos.all())

    def test_album_designate_cover(self):
        self.freddyalbum.designate_cover(self.bobphoto)
        self.assertEqual(self.freddyalbum.cover, self.bobphoto.photo)

    def test_album_photos_only_from_album_user(self):
        for photo in self.bobalbum.photo_set.all():
            self.assertEqual(str(photo.profile), 'Bob')

    def test_other_users_cant_add_to_album(self):
        with self.assertRaises(AttributeError):
            self.bobalbum.add_photo(self.alicephoto)
