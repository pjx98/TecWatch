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
import random
from django.conf import settings
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
        
        #settings.AXES_ENABLED = True
        
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
        
    
        
    #python manage.py test singhealth.tests.test_selenium.seleniumTest.test_user_full_cycle
    def test_user_full_cycle(self):
        """
        Test the full user experience from both the staff and tenant perspective.
        Sequence of events: 
        1. Staff login.
        2. Staff creates audit by adding necessary items to the dynamic checklist.
        3. Staff checks compliance practices and unchecks non-compliance practices.
        4. Staff creates complaint form based on the non-compliance practices.
        5. Tenant login
        6. Tenant sees complaint and uploads rectification.
        7. Staff login
        8. Staff accepts the rectification and resolves the complaint.

        """
        
        ###########################################################################################
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
        
        #################################################################################################################
        #Create audit for tenant
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
        
        #################################################################################################################
        #Create complaint by Staff
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
        time.sleep(2)
        
        # Return to staff homepage
        driver.find_element_by_name("loginId").click()
        time.sleep(2)
        
        # logout 
        driver.find_element_by_name('logout_btn').click()
        time.sleep(2)
        #################################################################################################################
        #Tenant upload rectification
        #login as tenant
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(self.tenant.username)
        time.sleep(2)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys(password)
        time.sleep(2)
        driver.find_element_by_css_selector('form input[type="submit"]').click()
        time.sleep(2)
        
        # In tenant homepage, click on view more details
        driver.find_element_by_name("complaintId").click()
        time.sleep(2)
        
        #Upload rectification
        driver.find_element_by_name("updateid").click()
        time.sleep(2)
        
        #Input Subject
        subject_input_rectification = driver.find_element_by_name("subject")
        subject_input_rectification.send_keys("Test_Rectification_1")
        time.sleep(2)
        
        #Upload Picture
        upload_field_rectification = driver.find_element_by_xpath("//input[@type='file']")
        upload_field_rectification.send_keys("D:\\Dropbox\\beautiful-sunset-tropical-beach-palm-260nw-1716193708.jpg")
        time.sleep(2)
        
        #Input comments
        comment_input_rectification = driver.find_element_by_name("comments")
        comment_input_rectification.send_keys("Test_Rectification_Comments")
        time.sleep(2)
        
        #Click submit, upload Rectification
        driver.find_element_by_name("comId").click()
        time.sleep(2)
        
        #In success page, returning to tenant homepage
        driver.find_element_by_name("loginId").click()
        time.sleep(2)
        
        #Logout from tenant homepage
        driver.find_element_by_name('logout_btn').click()
        time.sleep(2)
        
        #################################################################################################################
        #Staff resolving complaints
        #Login in as staff
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(self.staff.username)
        time.sleep(2)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys(password)
        time.sleep(2)
        driver.find_element_by_css_selector('form input[type="submit"]').click()
        time.sleep(2)
        
        #View related complaints
        driver.find_element_by_name("complaint").click()
        time.sleep(2)
        
        #click on view more details for the respective complaints
        driver.find_element_by_name("complaintId").click()
        time.sleep(2)
        
        #Resolve complaint
        driver.find_element_by_name("resolveid").click()
        time.sleep(2)
        
        #Return home
        driver.find_element_by_name("loginId").click()
        time.sleep(2)
        
        #Verify if complaint has been resolved
        driver.find_element_by_name("complaint").click()
        time.sleep(5)
        

        assert "Test_Complaint_1" in driver.page_source
    
    # python manage.py test singhealth.tests.test_selenium.seleniumTest.test_brute_force_login
    def test_brute_force_login(self):
        """
        Test login page by using invalid inputs generated from the random_string() (fuzzer) function.
        Test case will attempt to input as many invalid login credentials as it can.
        If the number of invaild login attempts exceeds the number of allowed_login_attempts, the user's ip address will be locked for 1hr to prevent further misuse.
        """
        
        # Fuzzer to generate invalid inputs
        def random_string():
            string_len = random.randint(10,50)
            input = ""
            for i in range(string_len+1):
                between_0_and_1 = random.random()
                input += chr(int(between_0_and_1 * 96 + 32))
                
            return str(input)
        
        settings.AXES_ENABLED = True
        max_login_attempts = settings.AXES_FAILURE_LIMIT
        
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/singhealth/'))
        
        for i in range(max_login_attempts):
            time.sleep(1)
            username_input = driver.find_element_by_name("username")
            username_input.send_keys(random_string())
            time.sleep(1)
            password_input = driver.find_element_by_name("password")
            password_input.send_keys(random_string())
            time.sleep(1)
            driver.find_element_by_css_selector('form input[type="submit"]').click()
            time.sleep(1)
        
        
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/singhealth/'))
        
        # Key in correct user credentials, expect lock out screen
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(self.tenant.username)
        time.sleep(2)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys(password)
        time.sleep(5)
        
        driver.find_element_by_css_selector('form input[type="submit"]').click()
        time.sleep(4)
        
        assert "Account locked" in driver.page_source

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
        
        driver.find_element_by_name('logout_btn').click()
        time.sleep(2)
        assert "Staff Homepage" in driver.page_source
        
        
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
        
        
    
        
    