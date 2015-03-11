from __future__ import print_function
from django.test import TestCase
from django.contrib.auth.models import User
from imager_images.models import Photo
from django.conf import settings


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
    photo = 'picture.jpeg'

#class AlbumFactory(factory.django.DjangoModelFactory):
#
#    class Meta:
#        model = Album
#
#    profile = UserFactory.create(username='Freddy').ImagerProfile


class TestHomepageViews(TestCase):

    STOCKPHOTO_URL = '/media/default_stock_photo_640_360.jpg'

    def setUp(self):
        self.bob = UserFactory.create()
        self.alice = UserFactory.create(username='Alice')
        self.bobphoto = PhotoFactory.create(profile=self.bob.ImagerProfile)
        self.publicbobphoto = PhotoFactory.create(profile=self.bob.ImagerProfile,
                                                  published='pb')
        #self.bobphoto2 = PhotoFactory.create(profile=self.bob.ImagerProfile)
        #self.alicephoto = PhotoFactory.create(profile=self.alice.ImagerProfile)
        #self.freddyalbum = AlbumFactory.create()
        #self.bobalbum = AlbumFactory.create(profile=self.bob.ImagerProfile)
        #self.bobalbum2 = AlbumFactory.create(profile=self.bob.ImagerProfile)

    def test_empty_url_finds_home_page(self):
        # import pdb; pdb.set_trace()
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
