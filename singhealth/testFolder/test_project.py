from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time 
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.contrib.auth.models import User
from django.test import Client
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from seleniumlogin import force_login

# Create your tests here.

staff_username = "staff"
tenant_username = "tenant"
password = "~1qaz2wsx"


class seleniumTest(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Edge(r'C:\\VS JAVA\\msedgedriver.exe')
        self.client = Client()
        self.user = User.objects.create_superuser(username=staff_username, password='password', email=None, is_active=True)
        self.user.set_password("password")
        #self.client.force_login(self.user)
        self.user.save()
        Staff = Group.objects.create(name='Staff')
        group = Group.objects.get(name="Staff")
        self.user.groups.add(group)



    def tearDown(self):
        self.driver.close()
        
    # @classmethod
    # def setUpClass(cls):
    #     super().setUpClass()
    #     cls.selenium = webdriver.Edge(r'C:\\VS JAVA\\msedgedriver.exe')
    #     #cls.selenium.implicitly_wait(10)

    # @classmethod
    # def tearDownClass(cls):
    #     cls.selenium.quit()
    #     super().tearDownClass()

    def test_login(self):
        driver = self.driver
        expected_url = "http://127.0.0.1:8000/singhealth/homestaff/"
        #self.user = authenticate(username="staff_5", password="~1qaz2wsx")

        #self.client.force_login(self.user)
        driver.get('%s%s' % (self.live_server_url, '/singhealth/'))
        time.sleep(2)
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(self.user.username)
        time.sleep(2)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys("~1qaz2wsx")
        time.sleep(2)
        driver.find_element_by_css_selector('form input[type="submit"]').click()
        time.sleep(2)
        assert "Staff Homepage" in driver.page_source
    
    # def test_staff(self):
    #     driver = self.driver
        
    #     driver.get('%s%s' % (self.live_server_url, '/singhealth/homestaff'))
    #     time.sleep(2)
    

            