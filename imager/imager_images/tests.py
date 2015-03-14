from __future__ import print_function
from django.test import TestCase
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

    profile = UserFactory.create(username='Freddy').ImagerProfile


class TestPhoto(TestCase):

    def setUp(self):
        self.bob = UserFactory.create()
        self.alice = UserFactory.create(username='Alice')
        self.bobphoto = PhotoFactory.create(profile=self.bob.ImagerProfile)
        self.alicephoto = PhotoFactory.create(profile=self.alice.ImagerProfile)

    def test_create_a_new_photo_file(self):
        self.assertEqual(self.bobphoto.profile.user, self.bob)
        self.assertEqual(self.bobphoto.title, 'No Title')
        self.assertEqual(self.bobphoto.description, 'No Description')
        self.assertEqual(self.bobphoto.published, 'pv')

    def test_photo_belongs_to_unique_user(self):
        self.assertEqual(self.bobphoto.profile.user, self.bob)

    def test_photo__str__returns_correct_string(self):
        self.assertEqual(self.bobphoto.__str__(),
                         'Photo Title: ' + self.bobphoto.title + '\nOwned by: '
                         + self.bobphoto.profile.user.username
                         )


class TestAlbum(TestCase):

    def setUp(self):
        self.bob = UserFactory.create()
        self.alice = UserFactory.create(username='Alice')
        self.bobphoto = PhotoFactory.create(profile=self.bob.ImagerProfile)
        self.bobphoto2 = PhotoFactory.create(profile=self.bob.ImagerProfile)
        self.alicephoto = PhotoFactory.create(profile=self.alice.ImagerProfile)
        self.freddyalbum = AlbumFactory.create()
        self.bobalbum = AlbumFactory.create(profile=self.bob.ImagerProfile)
        self.bobalbum2 = AlbumFactory.create(profile=self.bob.ImagerProfile)

    def test_album_has_a_profile(self):
        self.assertEqual(self.bobalbum.profile, self.bob.ImagerProfile)

    def test_new_album_is_empty(self):
        self.assertEqual(len(self.freddyalbum.photos.all()), 0)

    def test_album_attributes(self):
        self.assertEqual(self.freddyalbum.title, 'No Title')
        self.assertEqual(self.freddyalbum.description, 'No Description')
        self.assertEqual(self.freddyalbum.published, 'pv')

    def test_album_add_a_photo(self):
        self.bobalbum.add_photo(self.bobphoto)
        self.assertIn(self.bobphoto, self.bobalbum.show_photos())

    def test_album_designate_cover(self):
        self.freddyalbum.designate_cover(self.bobphoto)
        self.assertEqual(self.freddyalbum.cover, self.bobphoto)

    def test_album_show_photos(self):
        self.bobalbum.add_photo(self.bobphoto)
        for photo in self.bobalbum.show_photos():
            self.assertEqual(photo.profile.user, self.bob)

    def test_other_users_cant_add_to_album(self):
        with self.assertRaises(AttributeError):
            self.bobalbum.add_photo(self.alicephoto)

    def test_one_photo_in_multiple_albums(self):
        self.bobalbum.add_photo(self.bobphoto)
        self.bobalbum2.add_photo(self.bobphoto)
        self.assertIn(self.bobphoto, self.bobalbum.show_photos())
        self.assertIn(self.bobphoto, self.bobalbum2.show_photos())

    def test_multiple_photos_one_album(self):
        self.bobalbum.add_photo(self.bobphoto)
        self.bobalbum.add_photo(self.bobphoto2)
        self.assertIn(self.bobphoto, self.bobalbum.show_photos())
        self.assertIn(self.bobphoto2, self.bobalbum.show_photos())

    def test_album__str__returns_correct_string(self):
        self.assertEqual(self.bobalbum.__str__(),
                         'Album Title: ' + self.bobalbum.title + '\nOwned by: '
                         + self.bobalbum.profile.user.username
                         )
