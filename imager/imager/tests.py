from __future__ import print_function
from django.test import TestCase
from django.contrib.auth.models import User
from imager_images.models import Photo, Album
from django.test import Client
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
    photo = 'picture.jpeg'


class AlbumFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Album

    profile = UserFactory.create(username='Freddy').ImagerProfile


class TestHomepageViews(TestCase):

    STOCKPHOTO_URL = '/media/default_stock_photo_640_360.jpg'

    def setUp(self):
        self.bob = UserFactory.create()
        self.alice = UserFactory.create(username='Alice')
        self.bobphoto = PhotoFactory.create(profile=self.bob.ImagerProfile)
        self.publicbobphoto = PhotoFactory.create(profile=self.bob.ImagerProfile,
                                                  published='pb')

    def test_empty_url_finds_home_page(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')

    def test_home_page_photo_is_user_photo_or_default(self):
        response = self.client.get('/')
        self.assertEqual(
            response.context['random_photo'],
            self.publicbobphoto.photo.url)

    def test_home_page_photo_is_stock_if_no_user_photos(self):
        self.publicbobphoto.delete()
        response = self.client.get('/')
        self.assertEqual(
            response.context['random_photo'],
            self.STOCKPHOTO_URL)


class TestRegistrationViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_page_works(self):
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_new_user(self):
        self.client.post('/accounts/register/',
                         {'username': 'bobby',
                          'email': 'bobby@example.com',
                          'password1': 'test',
                          'password2': 'test'}
                         )
        self.assertEqual(len(User.objects.all()), 1)


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

    def test_profile_update_displays_correct_template(self):
        self.client.login(username='Bob', password='password')
        response = self.client.get('/profiles/update_profile/' + str(self.bob.pk) + '/')
        self.assertTemplateUsed(response, 'profiles/update_profile.html')

    def test_profile_update_unreachable_if_loggedout(self):
        response = self.client.get('/update_profile/' + str(self.bob.pk) + '/')
        self.assertTemplateNotUsed(response, 'update_profile.html')

    def test_PhotoUpdate_displays_correct_template(self):
        self.client.login(username='Bob', password='password')
        response = self.client.get('/update_photo/' + str(self.bobphoto.id) + '/')
        self.assertTemplateUsed(response, 'update_photo.html')

    def test_PhotoUpdate_unreachable_if_loggedout(self):
        response = self.client.get('/update_photo/' + str(self.bobphoto.id) + '/')
        self.assertTemplateNotUsed(response, 'update_photo.html')

    def test_PhotoDelete_displays_correct_template(self):
        self.client.login(username='Bob', password='password')
        response = self.client.get('/delete_photo/' + str(self.bobphoto.id) + '/')
        self.assertTemplateUsed(response, 'delete_form.html')

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
        response = self.client.get('/add_album/')
        self.assertTemplateUsed(response, 'create_form.html')

    def test_AlbumCreate_unreachable_if_loggedout(self):
        response = self.client.get('/add_album/')
        self.assertTemplateNotUsed(response, 'albums_form.html')

    def test_AlbumUpdate_displays_correct_template(self):
        self.client.login(username='Bob', password='password')
        self.bobalbum = AlbumFactory.create(profile=self.bob.ImagerProfile)
        response = self.client.get('/update_album/' + str(self.bobalbum.pk) + '/')
        self.assertTemplateUsed(response, 'update_album.html')

    def test_AlbumUpdate_unreachable_if_loggedout(self):
        self.bobalbum = AlbumFactory.create(profile=self.bob.ImagerProfile)
        response = self.client.get('/update_album/' + str(self.bobalbum.pk) + '/')
        self.assertTemplateNotUsed(response, 'update_album.html')

    def test_AlbumDelete_displays_correct_template(self):
        self.client.login(username='Bob', password='password')
        self.bobalbum = AlbumFactory.create(profile=self.bob.ImagerProfile)
        response = self.client.get('/delete_album/' + str(self.bobalbum.id) + '/')
        self.assertTemplateUsed(response, 'delete_form.html')

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
