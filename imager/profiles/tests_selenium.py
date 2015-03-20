from __future__ import print_function

from django.test import LiveServerTestCase
from selenium import webdriver

import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from django.contrib.auth.models import User
from imager_images.models import Photo, Album
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

    def test_login_goes_to_profile(self):
        # user presses login
        self.driver.get(self.live_server_url)
        self.driver.find_element_by_link_text("Login").click()

        # user enters credentials and submits form
        form = self.driver.find_element_by_tag_name("form")
        username_field = self.driver.find_element_by_id("id_username")
        username_field.send_keys("Bob")
        password_field = self.driver.find_element_by_id("id_password")
        password_field.send_keys("password")
        form.submit()

        # user see his profile page
        self.assertIn('Bob has', self.driver.page_source)
        self.assertIn('Bob is following', self.driver.page_source)
        self.assertIn('Personal Info', self.driver.page_source)

        # user clicks on edit profile
        self.driver.find_element_by_tag_name("button").click()

        # user sees profile edit page
        self.assertIn('Picture:', self.driver.page_source)
        self.assertIn('Change:', self.driver.page_source)
        self.assertIn('First Name', self.driver.page_source)

        # user edits name
        self.driver.find_element_by_id("id_first_name").send_keys("SuperBob")
        self.driver.find_element_by_tag_name("form").submit()
