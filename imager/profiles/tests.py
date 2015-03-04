from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
import os

from profiles.models import ImagerProfile


def create_user(username='testuser'):
    return User.objects.create_user(username)


class ImagerProfileMethodTests(TestCase):

    def test_ImagerProfile_active(self):
        bob1 = create_user('bob1')
        bob2 = create_user('bob2')
        bob3 = create_user('bob3')
        assert len(ImagerProfile.active()) == 3
        bob1.is_active = False
        bob1.save()
        assert len(ImagerProfile.active()) == 2
        bob2.is_active = False
        bob2.save()
        assert len(ImagerProfile.active()) == 1
        assert ImagerProfile.active()[0].user == bob3

    def test_create_user_creates_ImagerProfile(self):
        assert len(ImagerProfile.objects.all()) == 0
        bob = create_user('bob')
        assert len(ImagerProfile.objects.all()) == 1
        IP = ImagerProfile.objects.all()[0]
        assert IP.user == bob

    def test_delete_user_deletes_associated_IProfile(self):
        user = create_user('bob')
        user.delete()
        assert len(ImagerProfile.objects.all()) == 0

    def test_profile_user(self):
        user1 = create_user('bob')
        IPuser = ImagerProfile.objects.all()[0].user
        assert user1 == IPuser

    def test_is_active_with_active_user(self):
        bob = create_user('bob')
        IP = ImagerProfile.objects.get(user=bob)
        assert IP.is_active() is True

    def test_is_active_With_inactive_user(self):
        bob = create_user('bob')
        bob.is_active = False
        bob.save()
        IP = ImagerProfile.objects.get(user=bob)
        assert IP.is_active() is False

    def test_adding_profile_pic(self):
        bob = create_user('bob')
        IP = ImagerProfile.objects.get(user=bob)
        IP.picture = 'test'
        assert IP.picture == 'test'

    def test_following(self):
        bob = create_user('bob')
        alice = create_user('alice')
        IP_bob = ImagerProfile.objects.get(user=bob)
        IP_alice = ImagerProfile.objects.get(user=alice)
        IP_bob.follow(IP_alice)
        self.assertIn(IP_alice, IP_bob.following())

    def test_profile_followers_returns_proper_list(self):
        bob = create_user('bob')
        alice = create_user('alice')
        IP_bob = ImagerProfile.objects.get(user=bob)
        IP_alice = ImagerProfile.objects.get(user=alice)
        IP_bob.follow(IP_alice)
        self.assertIn(IP_alice, IP_bob.follows.all())
        self.assertNotIn(IP_bob, IP_alice.follows.all())

    def test_profile_unfollow_removes_followed(self):
        bob = create_user('bob')
        alice = create_user('alice')
        IP_bob = ImagerProfile.objects.get(user=bob)
        IP_alice = ImagerProfile.objects.get(user=alice)
        IP_bob.follow(IP_alice)
        IP_bob.unfollow(IP_alice)
        self.assertNotIn(IP_alice, IP_bob.follows.all())

    def test_unfollow_with_nonexistant_profile(self):
        IP_bob = create_user('bob')
        IP_bob.delete()
        alice = create_user('alice')
        IP_alice = ImagerProfile.objects.get(user=alice)
        with self.assertRaises(ValueError):
            IP_alice.unfollow(None)

    def test_followers_returns_proper_list_of_followers(self):
        bob = create_user('bob')
        alice = create_user('alice')
        IP_bob = ImagerProfile.objects.get(user=bob)
        IP_alice = ImagerProfile.objects.get(user=alice)
        IP_bob.follow(IP_alice)
        self.assertIn(IP_bob, IP_alice.followers())

    def test_block(self):
        bob = create_user('bob')
        alice = create_user('alice')
        IP_bob = ImagerProfile.objects.get(user=bob)
        IP_alice = ImagerProfile.objects.get(user=alice)
        IP_bob.follow(IP_alice)
        IP_alice.block(IP_bob)
        self.assertIn(IP_bob, IP_alice.blocked.all())

    def test_blocked_not_in_following(self):
        bob = create_user('bob')
        alice = create_user('alice')
        IP_bob = ImagerProfile.objects.get(user=bob)
        IP_alice = ImagerProfile.objects.get(user=alice)
        IP_bob.follow(IP_alice)
        IP_alice.block(IP_bob)
        self.assertNotIn(IP_alice, IP_bob.following())

    def test_blocked_not_in_followers(self):
        bob = create_user('bob')
        alice = create_user('alice')
        IP_bob = ImagerProfile.objects.get(user=bob)
        IP_alice = ImagerProfile.objects.get(user=alice)
        IP_bob.follow(IP_alice)
        IP_alice.block(IP_bob)
        self.assertNotIn(IP_bob, IP_bob.followers())

    def test_follow_blocked(self):
        bob = create_user('bob')
        alice = create_user('alice')
        IP_bob = ImagerProfile.objects.get(user=bob)
        IP_alice = ImagerProfile.objects.get(user=alice)
        IP_bob.follow(IP_alice)
        IP_alice.block(IP_bob)
        with self.assertRaises(ValueError):
            IP_bob.follow(IP_alice)

    def test_unfollow_blocked(self):
        bob = create_user('bob')
        alice = create_user('alice')
        IP_bob = ImagerProfile.objects.get(user=bob)
        IP_alice = ImagerProfile.objects.get(user=alice)
        IP_bob.follow(IP_alice)
        IP_alice.block(IP_bob)
        with self.assertRaises(ValueError):
            IP_bob.unfollow(IP_alice)
