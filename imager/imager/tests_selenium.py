from __future__ import print_function

from django.test import LiveServerTestCase
from selenium import webdriver

import os

from django.contrib.auth.models import User
import factory


SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'Bob'
    password = factory.PostGenerationMethodCall('set_password', 'password')


class TestLogin(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        super(TestLogin, self).setUp()
        self.bob = UserFactory.create()

    def tearDown(self):
        self.driver.quit()
        super(TestLogin, self).tearDown()

    def test_unauthorized_index(self):
        self.driver.get(self.live_server_url)
        self.assertIn('Login', self.driver.page_source)
        self.assertIn('Register', self.driver.page_source)

    def test_authorized_index(self):
        # try:
        self.driver.get(self.live_server_url)
        self.driver.find_element_by_link_text("Login").click()
        form = self.driver.find_element_by_tag_name("form")
        username_field = self.driver.find_element_by_id("id_username")
        username_field.send_keys("Bob")
        password_field = self.driver.find_element_by_id("id_password")
        password_field.send_keys("password")
        form.submit()
        self.assertIn('Bob', self.driver.page_source)
        self.assertIn('Library', self.driver.page_source)
        self.assertIn('Stream', self.driver.page_source)
        self.assertIn('Log out', self.driver.page_source)

        # user now logs off, a thoroughly satisfied user.
        self.driver.find_element_by_link_text("Log out").click()
        self.assertIn('Logged out', self.driver.page_source)

        # except Exception as e:
        #     self.driver.save_screenshot('SCREEN_DUMP_LOCATION.png')
        #     raise e

    def test_login_unauthorized_user(self):
        self.driver.get(self.live_server_url)
        self.driver.find_element_by_link_text("Login").click()
        form = self.driver.find_element_by_tag_name("form")
        username_field = self.driver.find_element_by_id("id_username")
        username_field.send_keys("Not a user")
        password_field = self.driver.find_element_by_id("id_password")
        password_field.send_keys("fake password")
        form.submit()
        self.assertIn('Please enter a correct username and password', self.driver.page_source)

    def test_random_image(self):
        self.driver.get(self.live_server_url)
        self.assertIn('default_stock_photo', self.driver.page_source)
