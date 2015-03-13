from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
import factory
from profiles.models import ImagerProfile
from imager_images.models import Photo, Album
from unittest import skip


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'bob1'
    password = factory.PostGenerationMethodCall('set_password', 'password')


class PhotoFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Photo

    profile = UserFactory.create(username='Bobby').ImagerProfile


class AlbumFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Album

    profile = UserFactory.create(username='Freddy').ImagerProfile


class ImagerProfileMethodTests(TestCase):

    def setUp(self):
        self.bob1 = UserFactory.create()
        self.bob2 = UserFactory.create(username='bob2')
        self.bob3 = UserFactory.create(username='bob3')
        self.IP_bob = UserFactory.create(username='bob').ImagerProfile
        self.IP_alice = UserFactory.create(username='alice').ImagerProfile

    def test_ImagerProfile_active(self):
        assert len(ImagerProfile.active()) == 5
        self.bob1.is_active = False
        self.bob1.save()
        assert len(ImagerProfile.active()) == 4
        self.bob2.is_active = False
        self.bob2.save()
        assert len(ImagerProfile.active()) == 3
        assert ImagerProfile.active()[0].user == self.bob3

    def test_create_user_creates_ImagerProfile(self):
        assert len(ImagerProfile.objects.all()) == 5
        bobbo = UserFactory.create(username='bobbo')
        assert len(ImagerProfile.objects.all()) == 6
        IP = ImagerProfile.objects.all()[5]
        assert IP.user == bobbo

    def test_delete_user_deletes_associated_IProfile(self):
        self.bob1.delete()
        assert len(ImagerProfile.objects.all()) == 4

    def test_profile_user(self):
        assert self.bob1 == self.bob1.ImagerProfile.user

    def test_is_active_with_active_user(self):
        assert self.bob1.ImagerProfile.is_active() is True

    def test_is_active_With_inactive_user(self):
        self.bob1.is_active = False
        self.bob1.save()
        IP = ImagerProfile.objects.get(user=self.bob1)
        assert IP.is_active() is False

    def test_adding_profile_pic(self):
        self.IP_bob.picture = 'test'
        assert self.IP_bob.picture == 'test'

    def test_following(self):
        self.IP_bob.follow(self.IP_alice)
        self.assertIn(self.IP_alice, self.IP_bob.following())

    def test_profile_followers_returns_proper_list(self):
        self.IP_bob.follow(self.IP_alice)
        self.assertIn(self.IP_alice, self.IP_bob.follows.all())
        self.assertNotIn(self.IP_bob, self.IP_alice.follows.all())

    def test_profile_unfollow_removes_followed(self):
        self.IP_bob.follow(self.IP_alice)
        self.IP_bob.unfollow(self.IP_alice)
        self.assertNotIn(self.IP_alice, self.IP_bob.follows.all())

    def test_unfollow_with_nonexistant_profile(self):
        with self.assertRaises(ValueError):
            self.IP_alice.unfollow(None)

    def test_followers_returns_proper_list_of_followers(self):
        self.IP_bob.follow(self.IP_alice)
        self.assertIn(self.IP_bob, self.IP_alice.followers())

    def test_block(self):
        self.IP_bob.follow(self.IP_alice)
        self.IP_alice.block(self.IP_bob)
        self.assertIn(self.IP_alice, self.IP_bob.blocked_by())

    def test_blocked_not_in_following(self):
        self.IP_bob.follow(self.IP_alice)
        self.IP_alice.block(self.IP_bob)
        self.assertNotIn(self.IP_alice, self.IP_bob.following())

    def test_blocked_not_in_followers(self):
        self.IP_bob.follow(self.IP_alice)
        self.IP_alice.block(self.IP_bob)
        self.assertNotIn(self.IP_bob, self.IP_bob.followers())

    def test_follow_blocked(self):
        self.IP_bob.follow(self.IP_alice)
        self.IP_alice.block(self.IP_bob)
        with self.assertRaises(ValueError):
            self.IP_bob.follow(self.IP_alice)

    def test_unfollow_blocked(self):
        self.IP_bob.follow(self.IP_alice)
        self.IP_alice.block(self.IP_bob)
        with self.assertRaises(ValueError):
            self.IP_bob.unfollow(self.IP_alice)

    def test_unblock_works_unblocking_follow(self):
        self.IP_bob.follow(self.IP_alice)
        self.IP_alice.block(self.IP_bob)
        self.IP_alice.unblock(self.IP_bob)
        self.assertIn(self.IP_bob, self.IP_alice.followers())

    def test_unblocked(self):
        self.IP_alice.block(self.IP_bob)
        self.IP_alice.unblock(self.IP_bob)
        self.assertNotIn(self.IP_bob, self.IP_alice.blocked.all())

    def test_unblocked_nonexistant_user_raises_error(self):
        with self.assertRaises(ValueError):
            self.IP_alice.unblock(None)

    def test_privacy_settings(self):
        self.assertTrue(self.IP_bob.name_priv)
        self.assertTrue(self.IP_bob.email_priv)
        self.assertTrue(self.IP_bob.picture_priv)
        self.assertTrue(self.IP_bob.phone_priv)
        self.assertTrue(self.IP_bob.birthday_priv)


class ImagerProfileImageTests(TestCase):
    def setUp(self):
        self.bob = UserFactory.create(username='Bob')
        self.alice = UserFactory.create(username='Alice')
        self.IP_bob = self.bob.ImagerProfile
        self.IP_alice = self.alice.ImagerProfile
        self.bobphoto = PhotoFactory.create(profile=self.bob.ImagerProfile,
                                            title="bob photo")
        self.bobphoto.published = 'pb'
        self.alicephoto = PhotoFactory.create(profile=self.alice.ImagerProfile,
                                              title="alice cool shot")
        self.alicephoto.published = 'pb'
        self.alicealbum = AlbumFactory.create(profile=self.alice.ImagerProfile)
        self.alicealbum.published = 'pb'

    def test_following_profile_sees_public_photos(self):
        self.IP_bob.follow(self.IP_alice)
        self.IP_bob.add_photo(self.alicephoto)
        self.assertIn(self.alicephoto, self.IP_bob.show_photos())

    def test_following_profile_does_not_get_private_photos(self):
        self.alicephoto.published = 'pv'
        self.alicephoto.save()
        with self.assertRaises(ValueError):
            self.IP_bob.add_photo(self.alicephoto)

    def test_user_sees_own_private_photos(self):
        self.bobphoto.published = 'pv'
        self.bobphoto.save()
        self.assertIn(self.bobphoto, self.IP_bob.show_all_photos())

    def test_following_profile_sees_public_albums(self):
        self.IP_bob.follow(self.IP_alice)
        self.IP_bob.add_album(self.alicealbum)
        self.assertIn(self.alicealbum, self.IP_bob.show_albums())

    def test_blocked_user_cant_get_albums(self):
        self.IP_bob.follow(self.IP_alice)
        self.IP_alice.block(self.IP_bob)
        with self.assertRaises(ValueError):
            self.IP_bob.add_album(self.alicealbum)

    def test_blocked_user_cant_get_photos(self):
        self.IP_bob.follow(self.IP_alice)
        self.IP_alice.block(self.IP_bob)
        with self.assertRaises(ValueError):
            self.IP_bob.add_photo(self.alicephoto)


class ProfilePageTests(TestCase):

    def setUp(self):
        self.bob = UserFactory.create(username='Bob')
        self.alice = UserFactory.create(username='Alice')
        self.IP_bob = self.bob.ImagerProfile
        self.IP_alice = self.alice.ImagerProfile
        self.bobphoto = PhotoFactory.create(profile=self.bob.ImagerProfile,
                                            title="bob photo",
                                            published='pb')
        self.bobalbum = AlbumFactory.create(profile=self.bob.ImagerProfile,
                                            title="bob is awesome",
                                            published='pb')
        self.alicephoto = PhotoFactory.create(profile=self.alice.ImagerProfile,
                                              title="alice cool shot",
                                              published='pb')
        self.alicealbum = AlbumFactory.create(profile=self.alice.ImagerProfile,
                                              title="alice awesome",
                                              published='pb')

        self.client = Client()

    def test_profile_page_NON_AUTHENTICATED(self):
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 302)  # REDIRECTS TO LOGIN

    def test_profile_page_LOGGEDIN(self):
        self.client.login(username='Bob', password='password')
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)

    def test_profile_page_displays_correct_template(self):
        self.client.login(username='Bob', password='password')
        response = self.client.get('/accounts/profile/')
        self.assertTemplateUsed(response, 'profile.html')

    @skip('profile uses cached thumbnails, difficult to test')
    def test_profile_page_displays_correct_profile_picture(self):
        self.client.login(username='Bob', password='password')
        response = self.client.get('/accounts/profile/')
        self.assertIn('text.txt', response.content)

    def test_profile_page_lists_correct_number_of_items(self):
        self.client.login(username='Bob', password='password')
        self.bobphoto2 = PhotoFactory.create(profile=self.bob.ImagerProfile,
                                             title="bob photo2")
        self.IP_alice.follow(self.IP_bob)
        self.IP_bob.follow(self.IP_alice)

        response = self.client.get('/accounts/profile/')
        self.assertIn('2 Photos', response.content)
        self.assertIn('1 Album', response.content)
        self.assertIn('1 Follower', response.content)
        self.assertIn('following 1 Person', response.content)

    def test_login_redirects_to_profile_page_upon_succesful_login(self):
        response = self.client.post(
            '/accounts/login',
            {'username': 'Bob', 'password': 'password'},
            follow=True
        )
        self.assertIn(
            (u'http://testserver/accounts/login/', 301),
            response.redirect_chain
        )

    def test_displayed_logged_in_as_name_is_link_to_profile_page(self):
        self.client.login(username='Bob', password='password')
        response = self.client.get('/accounts/profile/')
        self.assertIn(
            'href="/accounts/profile">Bob</a>', response.content
        )


class StreamPageTests(TestCase):
    def setUp(self):
        self.bob = UserFactory.create(username='Bob')
        self.alice = UserFactory.create(username='Alice')
        self.IP_bob = self.bob.ImagerProfile
        self.IP_alice = self.alice.ImagerProfile
        self.bobphoto = PhotoFactory.create(profile=self.bob.ImagerProfile,
                                            title="bob photo",
                                            published='pb')
        self.bobalbum = AlbumFactory.create(profile=self.bob.ImagerProfile,
                                            title="bob is awesome",
                                            published='pb')
        self.alicephoto = PhotoFactory.create(profile=self.alice.ImagerProfile,
                                              title="alice cool shot",
                                              published='pb')
        self.alicealbum = AlbumFactory.create(profile=self.alice.ImagerProfile,
                                              title="alice awesome",
                                              published='pb')

        self.client = Client()

    def test_stream_page_NON_AUTHENTICATED(self):
        response = self.client.get('/images/stream/')
        self.assertEqual(response.status_code, 404)

    def test_stream_page_LOGGEDIN(self):
        self.client.login(username='Bob', password='password')
        response = self.client.get('/images/stream/')
        self.assertEqual(response.status_code, 200)

    def test_stream_page_displays_correct_template(self):
        self.client.login(username='Bob', password='password')
        response = self.client.get('/images/stream/')
        self.assertTemplateUsed(response, 'profilestream.html')

    def test_stream_page_has_correct_subject_headers(self):
        self.client.login(username='Bob', password='password')
        self.bobphoto2 = PhotoFactory.create(profile=self.bob.ImagerProfile,
                                             title="bob photo2",)
        self.IP_alice.follow(self.IP_bob)
        self.IP_bob.follow(self.IP_alice)

        response = self.client.get('/images/stream/')
        self.assertIn("Bob's recent photos:", response.content)
        self.assertIn('Recently uploaded photos by Followed:', response.content)
        self.assertIn('uploaded on March 13, 2015', response.content)
        self.assertIn('uploaded by Alice on March 13, 2015', response.content)
