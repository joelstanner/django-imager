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

    def tearDown(self):
        self.driver.quit()
        super(TestLogin, self).tearDown()

    def test_unauthorized_index(self):
        self.driver.get(self.live_server_url)
        self.assertIn('Login', self.driver.page_source)
        self.assertIn('Register', self.driver.page_source)

    def test_authorized_index(self):
        self.driver.find_element_by_link_text("Login").click()
        username_field = self.driver.find_element_by_id("id_username")
        username_field.send_keys("Bob")
        password_field = self.driver.find_element_by_id("id_password")
        password_field.send_keys("password")
        self.assertIn('Bob', self.driver.page_source)
        
        
        
