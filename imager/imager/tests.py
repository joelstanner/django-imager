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


