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
from selenium.webdriver.support.ui import Select

# Create your tests here.

staff_username = "test_staff"
tenant_username = "test_tenant"
password = "~1qaz2wsx"


class seleniumTest(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(r'C:\\chromedriver.exe')
        # self.driver = webdriver.Edge(r'C:\\VS JAVA\\msedgedriver.exe')
        self.client = Client()
        
        #Create Staff User
        self.staff = User.objects.create_superuser(username=staff_username, password=password, email=None, is_active=True)
        self.staff.set_password(password)
        self.staff.save()
        Staff = Group.objects.create(name='Staff')
        group = Group.objects.get(name="Staff")
        self.staff.groups.add(group)
        
        #Create Tenant User
        self.tenant = User.objects.create_superuser(username=tenant_username, password=password, email=None, is_active=True)
        self.tenant.set_password(password)
        self.tenant.save()
        Tenant = Group.objects.create(name='Tenant')
        Outlet = Group.objects.create(name='West (F & B)')
        group = Group.objects.get(name="Tenant")
        self.tenant.groups.add(group)
        self.tenant.groups.add(Outlet)



    def tearDown(self):
        self.driver.close()
        
    # python manage.py test singhealth.tests.seleniumTest.test_login_staff
    def test_login_staff(self):
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/singhealth/'))
        time.sleep(2)
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(self.staff.username)
        time.sleep(2)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys(password)
        time.sleep(2)
        driver.find_element_by_css_selector('form input[type="submit"]').click()
        time.sleep(2)
        assert "Staff Homepage" in driver.page_source
    
    # python manage.py test singhealth.tests.seleniumTest.upload_complaint
    def upload_complaint(self):
        
        # Login staff user
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/singhealth/'))
        time.sleep(1)
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(self.staff.username)
        time.sleep(1)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys(password)
        time.sleep(1)
        driver.find_element_by_css_selector('form input[type="submit"]').click()
        time.sleep(1)
        
        # Create Complaint
        driver.find_element_by_name("create_complaint_btn").click()
        time.sleep(2)
        
        # Choose tenant from dropdown menu
        select = Select(driver.find_element_by_name('tenant'))
        select.select_by_visible_text(tenant_username)
        time.sleep(2)
        
        # Input subject field
        subject_input = driver.find_element_by_name("subject")
        subject_input.send_keys("Test_Complaint_1")
        time.sleep(2)
        
        # Upload Image
        upload_field = driver.find_element_by_xpath("//input[@type='file']")
        upload_field.send_keys("D:\\Dropbox\\beautiful-sunset-tropical-beach-palm-260nw-1716193708.jpg")
        time.sleep(2)
        
         # Input comment field
        comment_input = driver.find_element_by_name("comments")
        comment_input.send_keys("Test_Comments")
        time.sleep(2)
        
         # Input score field
        score_input = driver.find_element_by_name("score")
        score_input.send_keys(5)
        time.sleep(2)
        
         # Input deadline field
        deadline_input = driver.find_element_by_name("deadline")
        deadline_input.send_keys("2020-5-12")
        time.sleep(2)
        
         # Input Notes field
        notes_input = driver.find_element_by_name("notes")
        notes_input.send_keys("Test_Notes")
        time.sleep(2)
        
        # Submit Complaint
        driver.find_element_by_name("userId").click()
        time.sleep(2)
        
        # Verify if complaint is submitted successfully
        driver.find_element_by_name("complaintId").click()
        time.sleep(5)

        assert "Test_Complaint_1" in driver.page_source
    
    # python manage.py test singhealth.tests.seleniumTest.test_login_tenant
    def test_login_tenant(self):
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/singhealth/'))
        time.sleep(2)
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(self.tenant.username)
        time.sleep(2)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys(password)
        time.sleep(2)
        driver.find_element_by_css_selector('form input[type="submit"]').click()
        time.sleep(2)
        assert "Tenant Homepage" in driver.page_source

    # python manage.py test singhealth.tests.seleniumTest.upload_complaint
    def upload_rectification(self):
        
        # Login tenant user
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/singhealth/'))
        time.sleep(1)
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(self.tenant.username)
        time.sleep(1)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys(password)
        time.sleep(1)
        driver.find_element_by_css_selector('form input[type="submit"]').click()
        time.sleep(1)
        
        # Navigate: View first complaint encountered;  
        # Consider implementing automatic loop through all complaints later
        select = Select(driver.find_element_by_name('viewComplaintForm'))
        time.sleep(2)

        # Upload rectification
        driver.find_element_by_name("updateid").click()
        time.sleep(2)
        
        # Input subject field
        subject_input = driver.find_element_by_name("subject")
        subject_input.send_keys("Test_Complaint_1")
        time.sleep(2)
        
        # Upload Image
        upload_field = driver.find_element_by_xpath("//input[@type='file']")
        upload_field.send_keys("D:\\Term5\\50.003\\Project\\Techwatch_images\\beautiful-sunset-tropical-beach-palm-260nw-1716193708.jpg")
        time.sleep(2)
        
         # Input comment field
        comment_input = driver.find_element_by_name("comments")
        comment_input.send_keys("Test_Comments")
        time.sleep(2)
        
        # Upload Complaint
        driver.find_element_by_name("comId").click()
        time.sleep(2)
        
        # Verify if complaint is submitted successfully
        driver.find_element_by_name("complaintId").click()
        time.sleep(5)

        assert "Rectification submitted successfully" in driver.page_source