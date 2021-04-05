from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time 
from django.contrib.staticfiles.testing import LiveServerTestCase, StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.test import Client
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from seleniumlogin import force_login
from selenium.webdriver.support.ui import Select
from singhealth.models import Complaint
from checklist.models import Checklist, ChecklistItem
import datetime

# Create your tests here.

staff_username = "test_staff"
tenant_username = "test_tenant"
password = "~1qaz2wsx"


class seleniumTest(StaticLiveServerTestCase):
    
    def setUp(self):
        self.driver = webdriver.Edge(r'C:\\VS JAVA\\msedgedriver.exe')
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
        
        self.checklist = Checklist.objects.create(category='fnb')
        
        # self.test_complaint_form = Complaint.objects.create(status='Open',
        #                                                subject='test_subject',
        #                                                score=5,
        #                                                deadline='2020-04-12',
        #                                                date_created='2020-04-01',
        #                                                notes='test_notes',
        #                                                staff=staff,
        #                                                tenant=tenant,
        #                                                )
    
    


    def tearDown(self):
        self.driver.close()
        
    # python manage.py test singhealth.tests.test_selenium.seleniumTest.test_login_staff
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
        
    #python manage.py test singhealth.tests.test_selenium.seleniumTest.test_upload_checklist
    def test_upload_checklist(self):
        
        #login staff
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
        
        #add items to checklist
        driver.find_element_by_name("add_items_btn").click()
        time.sleep(2)
        
        # Input Description
        description_input = driver.find_element_by_name("description")
        description_input.send_keys("Floor slippery")
        time.sleep(2)
        
        #submit description
        driver.find_element_by_name("submit_description").click()
        time.sleep(2)
        
        # Input Description
        description_input = driver.find_element_by_name("description")
        description_input.send_keys("Tables are dirty")
        time.sleep(2)
        
        #submit description
        driver.find_element_by_name("submit_description").click()
        time.sleep(2)
        
        #return to homepage
        driver.find_element_by_name("return").click()
        time.sleep(2)
        
        # Update checklist
        driver.find_element_by_name("update_fnb_btn").click()
        time.sleep(2)
        
        #add items
        driver.find_element_by_id("id_items_0").click()
        driver.find_element_by_id("id_items_1").click()
        time.sleep(2)
        
        #submit
        driver.find_element_by_name("update").click()
        time.sleep(2)
        
        #go back homepage
        driver.find_element_by_name("return").click()
        time.sleep(2)
        
        # go to tenant view audits
        driver.find_element_by_name("audit").click()
        time.sleep(2)
        
        # New audit
        driver.find_element_by_name("tenantId").click()
        time.sleep(2)
        
        # Choose F&B option
        driver.find_element_by_id("fnb").click()
        time.sleep(2)
        
        #add items in audit
        driver.find_element_by_id("id_items_0").click()
        driver.find_element_by_id("id_items_1").click()
        time.sleep(2)
        
        #submit items for audit
        driver.find_element_by_name("category").click()
        time.sleep(2)
        
        
        # go to tenant view audits
        driver.find_element_by_name("audit").click()
        time.sleep(2)
        
        driver.find_element_by_name("return").click()
        time.sleep(2)
        
        ########################################################
        
        # Create Complaint
        driver.find_element_by_name("create_complaint_btn").click()
        time.sleep(2)
        
        
        # Choose tenant from dropdown menu
        select = Select(driver.find_element_by_name('tenant'))
        select.select_by_visible_text(tenant_username)
        time.sleep(2)
        
        #choose checklist
        select = Select(driver.find_element_by_name('checklist'))
        select.select_by_visible_text(str(datetime.date.today()) + '; Score: 2 (test_tenant)')
        time.sleep(2)
        
        # Input deadline field
        deadline_input = driver.find_element_by_name("deadline")
        deadline_input.send_keys("03/28/2022")
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
        
        #  # Input score field
        # score_input = driver.find_element_by_name("score")
        # score_input.send_keys(5)
        # time.sleep(2)
        
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
        
        
        
    
    # python manage.py test singhealth.tests.test_selenium.seleniumTest.upload_complaint
    def upload_complaint(self):
        
        # self.checklist_items = ChecklistItem.objects.create(description='Tables are dirty')
        
        # self.checklist = Checklist.objects.create(category='fnb',
        #                                           items= self.checklist_items)
        
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
        time.sleep(10)
        
        # Create Complaint
        driver.find_element_by_name("create_complaint_btn").click()
        time.sleep(2)
        
        
        # Choose tenant from dropdown menu
        select = Select(driver.find_element_by_name('tenant'))
        select.select_by_visible_text(tenant_username)
        time.sleep(2)
        
        #choose checklist
        select = Select(driver.find_element_by_name('checklist'))
        select.select_by_visible_text('2021-03-26; Score: 2 (test_tenant)')
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
        
        #  # Input score field
        # score_input = driver.find_element_by_name("score")
        # score_input.send_keys(5)
        # time.sleep(2)
        
         # Input deadline field
        deadline_input = driver.find_element_by_name("deadline")
        deadline_input.send_keys("03/28/2021")
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
    
    # python manage.py test singhealth.tests.test_selenium.seleniumTest.test_login_tenant
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

    # python manage.py test singhealth.tests.test_selenium.seleniumTest.upload_rectification
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