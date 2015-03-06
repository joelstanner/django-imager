from django.test import TestCase
from django.contrib.auth.models import User
import factory
from profiles.models import ImagerProfile
from imager_images.models import Photo, Album


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'bob1'


class PhotoFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Photo

    profile = UserFactory.create(username='Bobby').ImagerProfile


class AlbumFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Album

    user = UserFactory.create(username='Freddy')


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


class ImagerProfileImageTests(TestCase):
    def setUp(self):
        self.bob = UserFactory.create(username='Bob')
        self.alice = UserFactory.create(username='Alice')
        self.IP_bob = self.bob.ImagerProfile
        self.IP_alice = self.alice.ImagerProfile
        self.bobphoto = PhotoFactory.create(profile=self.bob.ImagerProfile)
        self.alicephoto = PhotoFactory.create(profile=self.alice.ImagerProfile)

    def test_following_profile_sees_public_photos(self):
        pass

    def test_following_profile_does_not_see_private_photos(self):
        pass

    def test_following_profile_sees_public_albums(self):
        pass

    def test_following_profile_does_not_see_private_albums(self):
        pass

    def test_only_one_other_profile_sees_shared_photos(self):
        pass

    def test_only_one_other_profile_sees_shared_albums(self):
        pass

    def test_blocked_user_cant_see_photos_or_albumse(self):
        pass












