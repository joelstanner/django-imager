from __future__ import print_function

from django.test import TestCase, LiveServerTestCase
from selenium import webdriver


from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from imager_images.models import Photo, Album
from django.test import Client
import factory


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
