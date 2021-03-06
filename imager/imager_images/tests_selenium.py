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


class TestImagerPages(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        super(TestImagerPages, self).setUp()
        self.bob = UserFactory.create()

    def tearDown(self):
        self.driver.quit()
        super(TestImagerPages, self).tearDown()

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

        # user clicks library
        self.driver.find_element_by_partial_link_text("Library").click()

        # user see library page
        self.assertIn("Bob's Library", self.driver.page_source)

        # user clicks Stream
        self.driver.find_element_by_partial_link_text("Stream").click()

        # user sees stream page
        self.assertIn("Bob's recent photos", self.driver.page_source)

        # user goes back to library page and adds a photo
        self.driver.find_element_by_partial_link_text("Library").click()
        self.driver.find_element_by_link_text("add photo").click()

        # user sees add photo page
        self.assertIn("Title", self.driver.page_source)
        self.assertIn("Description", self.driver.page_source)

        # user adds photo
        self.driver.find_element_by_id("id_photo").send_keys(os.getcwd()+"/PIA14944_SaturnHur1000.jpg")
        form = self.driver.find_element_by_tag_name("form")
        form.submit()

        # user is redirected to library page with a thumbnail of the new photo
        self.assertIn("update_photo", self.driver.page_source)

        # user goes to album page and sets cover to new photo
        self.driver.find_element_by_link_text("add album").click()
        self.driver.find_element_by_id("id_cover_photo").click()
        self.driver.find_element_by_xpath('//*[@id="id_cover_photo"]/option[2]').click()

        form = self.driver.find_element_by_tag_name("form")
        form.submit()

        # user is redirected to library page with a thumbnail of the new album
        self.assertIn("update_album", self.driver.page_source)
