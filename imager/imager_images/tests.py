from __future__ import print_function
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from models import Photo, Album
import factory


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'Bob'
    password = factory.PostGenerationMethodCall('set_password', 'password')


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

    def test_album_designate_cover_photo(self):
        self.freddyalbum.designate_cover(self.bobphoto)
        self.assertEqual(self.freddyalbum.cover_photo, self.bobphoto)

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


class TestImagerViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.bob = UserFactory.create()
        self.alice = UserFactory.create(username='Alice')
        self.IP_bob = self.bob.ImagerProfile
        self.bobphoto = PhotoFactory.create(profile=self.bob.ImagerProfile,
                                            title="bob photo",
                                            published='pb')
        self.bobalbum = AlbumFactory.create(profile=self.bob.ImagerProfile,
                                            title="bob awesome album",
                                            published='pb')

    def test_PhotoUpdate_displays_correct_template(self):
        self.client.login(username='Bob', password='password')
        response = self.client.get('/images/update_photo/' + str(self.bobphoto.id) + '/')
        self.assertTemplateUsed(response, 'imager_images/update_photo.html')

    def test_PhotoUpdate_unreachable_if_loggedout(self):
        response = self.client.get('/update_photo/' + str(self.bobphoto.id) + '/')
        self.assertTemplateNotUsed(response, 'update_photo.html')

    def test_PhotoDelete_displays_correct_template(self):
        self.client.login(username='Bob', password='password')
        response = self.client.get('/images/delete_photo/' + str(self.bobphoto.id) + '/')
        self.assertTemplateUsed(response, 'imager_images/delete_form.html')

    def test_PhotoDelete_unreachable_if_loggedout(self):
        response = self.client.get('/delete_photo/' + str(self.bobphoto.id) + '/')
        self.assertTemplateNotUsed(response, 'delete_photo.html')

    def test_PhotoDelete_actually_deletes_photo(self):
        self.client.login(username='Bob', password='password')
        bobphoto_id = self.bobphoto.id
        self.client.post('/delete_photo/' + str(self.bobphoto.id) + '/')
        response = self.client.get('/delete_photo/' + str(bobphoto_id) + '/')
        self.assertTemplateNotUsed(response, 'delete_photo.html')

    def test_PhotoDelete_not_usable_on_other_users_photo(self):
        self.client.login(username='Bob', password='password')
        self.alicephoto = PhotoFactory.create(profile=self.alice.ImagerProfile,
                                              title="alice cool shot",
                                              published='pb')
        response = self.client.post('/delete_photo/' + str(self.alicephoto.id) + '/')
        self.assertTrue(self.alicephoto.id)
        self.assertTemplateNotUsed(response, 'delete_photo.html')

    def test_AlbumCreate_displays_correct_template(self):
        self.client.login(username='Bob', password='password')
        response = self.client.get('/images/add_album/')
        self.assertTemplateUsed(response, 'imager_images/create_form.html')

    def test_AlbumCreate_unreachable_if_loggedout(self):
        response = self.client.get('/images/add_album/')
        self.assertTemplateNotUsed(response, 'imager_images/albums_form.html')

    def test_AlbumUpdate_displays_correct_template(self):
        self.client.login(username='Bob', password='password')
        self.bobalbum = AlbumFactory.create(profile=self.bob.ImagerProfile)
        response = self.client.get('/images/update_album/' + str(self.bobalbum.pk) + '/')
        self.assertTemplateUsed(response, 'imager_images/update_album.html')

    def test_AlbumUpdate_unreachable_if_loggedout(self):
        self.bobalbum = AlbumFactory.create(profile=self.bob.ImagerProfile)
        response = self.client.get('/update_album/' + str(self.bobalbum.pk) + '/')
        self.assertTemplateNotUsed(response, 'update_album.html')

    def test_AlbumDelete_displays_correct_template(self):
        self.client.login(username='Bob', password='password')
        self.bobalbum = AlbumFactory.create(profile=self.bob.ImagerProfile)
        response = self.client.get('/images/delete_album/' + str(self.bobalbum.id) + '/')
        self.assertTemplateUsed(response, 'imager_images/delete_form.html')

    def test_AlbumDelete_unreachable_if_loggedout(self):
        self.bobalbum = AlbumFactory.create(profile=self.bob.ImagerProfile)
        response = self.client.get('/delete_album/' + str(self.bobalbum.id) + '/')
        self.assertTemplateNotUsed(response, 'delete_album.html')

    def test_AlbumDelete_actually_deletes_album(self):
        self.client.login(username='Bob', password='password')
        bobalbum_id = self.bobalbum.id
        self.client.post('/delete_album/' + str(self.bobalbum.id) + '/')
        response = self.client.get('/album_photo/' + str(bobalbum_id) + '/')
        self.assertTemplateNotUsed(response, 'delete_album.html')

    def test_AlbumDelete_not_usable_on_other_users_album(self):
        self.client.login(username='Bob', password='password')
        self.alicealbum = AlbumFactory.create(profile=self.alice.ImagerProfile,
                                              title="alice cool album",
                                              published='pb')
        response = self.client.post('/delete_album/' + str(self.alicealbum.id) + '/')
        self.assertTrue(self.alicealbum.id)
        self.assertTemplateNotUsed(response, 'delete_album.html')

