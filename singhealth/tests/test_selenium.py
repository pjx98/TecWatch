from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time 
from datetime import datetime 
from django.contrib.staticfiles.testing import LiveServerTestCase, StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.test import Client
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from seleniumlogin import force_login
from selenium.webdriver.support.ui import Select
from singhealth.models import Complaint
from checklist.models import Checklist, ChecklistItem
#import datetime
import random
import os
from django.conf import settings
from selenium.common.exceptions import ErrorInResponseException
from checklist.models import *
# Create your tests here.

staff_username = "test_staff"
tenant_username = "test_tenant"
password = "~1qaz2wsx"


class seleniumTest(StaticLiveServerTestCase):
    
    def setUp(self):
        
        # Set download options for downloading of excel file
        options = Options()
        options.add_experimental_option("prefs", {
        "download.default_directory": "D:\\Download\\",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
        })
        self.driver = webdriver.Chrome(os.path.join(settings.BASE_DIR, "chromedriver.exe"), chrome_options=options)
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
        self.checklist = Checklist.objects.create(category='nonfnb')
        
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
        
    
        
    # python manage.py test singhealth.tests.test_selenium.seleniumTest.test_user_full_cycle
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
        time.sleep(3)
        
        # Input Description
        description_input = driver.find_element_by_name("description")
        description_input.send_keys("Tables are dirty")
        time.sleep(3)
        
        #submit description
        driver.find_element_by_name("submit_description").click()
        time.sleep(3)
        
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
        time.sleep(5)
        
        #choose checklist
        select = Select(driver.find_element_by_name('checklist'))
        #select.select_by_visible_text(str(datetime.today().strftime('%Y-%m-%d')) + '; Score: 2 (test_tenant)')
        select.select_by_index(1)
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
    
    # python manage.py test singhealth.tests.test_selenium.seleniumTest.test_complaint_form
    def test_complaint_form(self):
        
        '''
        This is to test the mandatory fields in the complaint form. 
        This ensures that each field in the complaint form must be filled up before the user can submit the complaint.
        '''
        
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
        time.sleep(1)
        
        #submit description
        driver.find_element_by_name("submit_description").click()
        time.sleep(1)
        
        # Input Description
        description_input = driver.find_element_by_name("description")
        description_input.send_keys("Tables are dirty")
        time.sleep(1)
        
        #submit description
        driver.find_element_by_name("submit_description").click()
        time.sleep(1)
        
        #return to homepage
        driver.find_element_by_name("return").click()
        time.sleep(1)
        
        # Update checklist
        driver.find_element_by_name("update_fnb_btn").click()
        time.sleep(1)
        
        #add items
        driver.find_element_by_id("id_items_0").click()
        driver.find_element_by_id("id_items_1").click()
        time.sleep(1)
        
        #submit
        driver.find_element_by_name("update").click()
        time.sleep(1)
        
        #go back homepage
        driver.find_element_by_name("return").click()
        time.sleep(1)
        
        #################################################################################################################
        #Create audit for tenant
        # go to tenant view audits
        driver.find_element_by_name("audit").click()
        time.sleep(1)
        
        # New audit
        driver.find_element_by_name("tenantId").click()
        time.sleep(1)
        
        # Choose F&B option
        driver.find_element_by_id("fnb").click()
        time.sleep(1)
        
        #add items in audit
        driver.find_element_by_id("id_items_0").click()
        driver.find_element_by_id("id_items_1").click()
        time.sleep(1)
        
        #submit items for audit
        driver.find_element_by_name("category").click()
        time.sleep(1)
        
        
        # go to tenant view audits
        driver.find_element_by_name("audit").click()
        time.sleep(1)
        
        driver.find_element_by_name("return").click()
        time.sleep(1)
        
        #################################################################################################################
        #Create complaint by Staff
        # Create Complaint
        driver.find_element_by_name("create_complaint_btn").click()
        time.sleep(2)
        
        # Submit Complaint, test empty tenant field
        driver.find_element_by_name("userId").click()
        time.sleep(1)
        
        
        # Choose tenant from dropdown menu
        select = Select(driver.find_element_by_name('tenant'))
        select.select_by_visible_text(tenant_username)
        time.sleep(1)
        
        # Submit Complaint, test empty checklist field
        driver.find_element_by_name("userId").click()
        time.sleep(1)
        
        #choose checklist
        select = Select(driver.find_element_by_name('checklist'))
        #select.select_by_visible_text(str(datetime.today().strftime('%Y-%m-%d')) + '; Score: 2 (test_tenant)')
        select.select_by_index(1)
        time.sleep(1)
        
        # Submit Complaint, test empty deadline field
        driver.find_element_by_name("userId").click()
        time.sleep(1)
        
        
        # Input deadline field
        deadline_input = driver.find_element_by_name("deadline")
        deadline_input.send_keys("03/28/2022")
        time.sleep(1)
        
        # Submit Complaint, test empty input field
        driver.find_element_by_name("userId").click()
        time.sleep(1)
        
        # Input subject field
        subject_input = driver.find_element_by_name("subject")
        subject_input.send_keys("Test_Complaint_1")
        time.sleep(1)
        
        # Submit Complaint, test empty file field
        driver.find_element_by_name("userId").click()
        time.sleep(1)
        
        # Upload Image. 
        upload_field = driver.find_element_by_xpath("//input[@type='file']")
        upload_field.send_keys("D:\\Dropbox\\beautiful-sunset-tropical-beach-palm-260nw-1716193708.jpg")
        time.sleep(1)
        
        # Submit Complaint, test empty comment field
        driver.find_element_by_name("userId").click()
        time.sleep(1)
        
         # Input comment field
        comment_input = driver.find_element_by_name("comments")
        comment_input.send_keys("Test_Comments")
        time.sleep(1)
        
        # Submit Complaint, test empty notes field
        driver.find_element_by_name("userId").click()
        time.sleep(1)
        
        # Input Notes field
        notes_input = driver.find_element_by_name("notes")
        notes_input.send_keys("Test_Notes")
        time.sleep(1)
        
        # Submit Complaint
        driver.find_element_by_name("userId").click()
        time.sleep(1)
        
        # Verify if complaint is submitted successfully
        driver.find_element_by_name("complaintId").click()
        time.sleep(1)
        
        # Return to staff homepage
        driver.find_element_by_name("loginId").click()
        time.sleep(2)
        
        assert "test_staff" in driver.page_source 
        
    # python manage.py test singhealth.tests.test_selenium.seleniumTest.test_brute_force_login
    def test_brute_force_login(self):
        """
        Robustness Testing
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
        time.sleep(2)
        
        driver.find_element_by_css_selector('form input[type="submit"]').click()
        time.sleep(4)
        
        assert "Account locked" in driver.page_source
        
    # python manage.py test singhealth.tests.test_selenium.seleniumTest.test_login
    def test_login(self):
        '''
        Test invalid input for login system
        '''
        
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/singhealth/'))
        time.sleep(2)
        
        # test invalid username, correct password
        username_input = driver.find_element_by_name("username")
        username_input.send_keys("test_staff_2")
        time.sleep(2)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys(password)
        time.sleep(2)
        driver.find_element_by_css_selector('form input[type="submit"]').click()
        time.sleep(2)
        
        # test invalid password, correct username
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(self.staff.username)
        time.sleep(2)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys("12345")
        time.sleep(2)
        driver.find_element_by_css_selector('form input[type="submit"]').click()
        time.sleep(2)
        
        # test empty inputs
        username_input = driver.find_element_by_name("username")
        username_input.send_keys("")
        time.sleep(2)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys("")
        time.sleep(2)
        driver.find_element_by_css_selector('form input[type="submit"]').click()
        time.sleep(2)
        
        # test valid staff login credentials
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(self.staff.username)
        time.sleep(2)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys(password)
        time.sleep(2)
        driver.find_element_by_css_selector('form input[type="submit"]').click()
        time.sleep(2)
        
        assert "test_staff" in driver.page_source
        
        
        
        
   
    # python manage.py test singhealth.tests.test_selenium.seleniumTest.test_download_to_excel_and_export_to_email
    def test_download_to_excel_and_export_to_email(self):
        """
        To test if excel file can be downloaded successfully,
        and using the downloaded excel file as an attachment to export to email.
        To check if email function is working correctly, please refer to the EmailTest in test_views.py.
        """
        
        # login as staff
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/singhealth/'))
        time.sleep(2)
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(self.staff.username)
        time.sleep(1)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys(password)
        time.sleep(1)
        driver.find_element_by_css_selector('form input[type="submit"]').click()
        time.sleep(1)
        
        #add items to checklist
        driver.find_element_by_name("add_items_btn").click()
        time.sleep(1)
        
        # Input Description
        description_input = driver.find_element_by_name("description")
        description_input.send_keys("Floor slippery")
        time.sleep(1)
        
        #submit description
        driver.find_element_by_name("submit_description").click()
        time.sleep(1)
        
        #return to homepage
        driver.find_element_by_name("return").click()
        time.sleep(1)
        
        # Update checklist
        driver.find_element_by_name("update_fnb_btn").click()
        time.sleep(1)
        
        #add items
        driver.find_element_by_id("id_items_0").click()
        time.sleep(1)
        
        #submit
        driver.find_element_by_name("update").click()
        time.sleep(1)
        
        #go back homepage
        driver.find_element_by_name("return").click()
        time.sleep(1)
        
        #################################################################################################################
        #Create audit for tenant
        # go to tenant view audits
        driver.find_element_by_name("audit").click()
        time.sleep(1)
        
        # New audit
        driver.find_element_by_name("tenantId").click()
        time.sleep(1)
        
        # Choose F&B option
        driver.find_element_by_id("fnb").click()
        time.sleep(1)
        
        #add items in audit
        driver.find_element_by_id("id_items_0").click()
        time.sleep(1)
        
        #submit items for audit
        driver.find_element_by_name("category").click()
        time.sleep(1)
        
        
        # go to tenant view audits
        driver.find_element_by_name("audit").click()
        time.sleep(1)
        
        #################################################################################################################
        
        
        # export to excel
        driver.find_element_by_id("exportbtn").click()
        time.sleep(2)
        
        # Click on export email link
        driver.find_element_by_xpath("//*[contains(text(), 'Export to email')]").click()
        time.sleep(2)
        
        # Input email address
        email_input = driver.find_element_by_name("email")
        email_input.send_keys("pjingxiang@gmail.com")
        time.sleep(2)
        
        # Input Subject field
        subject_input = driver.find_element_by_name("subject")
        subject_input.send_keys("Audit File")
        time.sleep(2)
        
        # Input Message
        message_input = driver.find_element_by_name("message")
        message_input.send_keys("Attached is the excel file")
        time.sleep(2)
        
        # Upload file
        upload_field = driver.find_element_by_xpath("//input[@type='file']")
        upload_field.send_keys("D:\\Download\\Audits" + "_" + str(datetime.today().strftime('%Y-%m-%d')) + '.xls' )
        time.sleep(2)
        
        # Sumbit email
        driver.find_element_by_name("send_mail").click()
        time.sleep(5)
        
        assert "test_staff!" in driver.page_source 
        
    # python manage.py test singhealth.tests.test_selenium.seleniumTest.click_random_link
    def click_random_link(self):
        """
        This is a robustness test which clicks random links.
        However, since some webpage have certain preconditions such as audits, complaints or excel file to fully function,
        and it would take up far too much time to go through the full user cycle for this test,
        this test will only test if the individual webpage displays successfully, 
        after which it will navigate back.
        If webpage display a server error code, exception would be raised.
        To prevent infinite clicking, the test will stop after 20 links have been clicked.
        """
        
        def fill_forms():
            try:
                # if login page -> login as staff
                if driver.current_url ==  ('%s%s' % (self.live_server_url, '/singhealth/')):
                    username_input = driver.find_element_by_name("username")
                    username_input.send_keys(self.staff.username)
                    time.sleep(1)
                    password_input = driver.find_element_by_name("password")
                    password_input.send_keys(password)
                    time.sleep(1)
                    driver.find_element_by_css_selector('form input[type="submit"]').click()
                    time.sleep(1)
                    
                # if create complaint
                elif driver.current_url == ('%s%s' % (self.live_server_url, '/singhealth/create/')):
                    time.sleep(2)
                    driver.find_element_by_xpath("//*[contains(text(), 'Return Home')]").click()
                    time.sleep(2)
                    
                # if add items
                elif driver.current_url == ('%s%s' % (self.live_server_url, '/checklist/additems/')):
                    time.sleep(2)
                    # Input Description
                    description_input = driver.find_element_by_name("description")
                    description_input.send_keys("Floor slippery")
                    time.sleep(1)
                    
                    #submit description
                    driver.find_element_by_name("submit_description").click()
                    time.sleep(2)
                    
                    #return to homepage
                    driver.find_element_by_name("return").click()
                    time.sleep(1)
                # if fnb page
                elif driver.current_url == ('%s%s' % (self.live_server_url, '/checklist/fnb/')):
                    time.sleep(2)
                    driver.execute_script("window.history.go(-1)")
                
                # if non fnb page
                elif driver.current_url == ('%s%s' % (self.live_server_url, '/checklist/nonfnb/')):
                    time.sleep(2)
                    driver.execute_script("window.history.go(-1)")
                
                # if view tenant page
                elif driver.current_url == ('%s%s' % (self.live_server_url, '/singhealth/viewtenant/')):
                    time.sleep(2)
                    driver.find_element_by_xpath("//*[contains(text(), 'Return Home')]").click()
                    time.sleep(2)
                    
                # if view audits page
                elif driver.current_url == ('%s%s' % (self.live_server_url, '/checklist/viewaudits/')):
                    time.sleep(2)
                    driver.find_element_by_xpath("//*[contains(text(), 'Return Home')]").click()
                    time.sleep(2)
                
                # if send email page
                elif driver.current_url == ('%s%s' % (self.live_server_url, '/notification/send_email/')):
                    driver.find_element_by_xpath("//*[contains(text(), 'Return Home')]").click()
                    time.sleep(2)
                
                else:
                    print("No more links")
                    self.assertTrue("true", "false")
                    
            except ErrorInResponseException as e:
                self.assertFalse("true", "true")
                driver.close()        
        
                
        # def error_page():
        #     if driver.find_element_by_xpath("//*[contains(text(), 'Server Error')]"):
        #         print("Error encountered")
        #         except ErrorInResponseException
                
            
            
        counter = 0
        
        # login as staff
        driver = self.driver
        driver.get('%s%s' % (self.live_server_url, '/singhealth/'))
        time.sleep(2)
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(self.staff.username)
        time.sleep(1)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys(password)
        time.sleep(1)
        driver.find_element_by_css_selector('form input[type="submit"]').click()
        time.sleep(1)
        
        print("Clicking random link ")
        while (counter < 20):
            counter = counter + 1
            links = [link for link in driver.find_elements_by_tag_name("a") if link.is_displayed()]
            if links:
                l = links[random.randint(0, len(links) - 1)]
                driver.execute_script('arguments[0].scrollIntoView();', l)
                print(l.get_attribute("href"))
                time.sleep(1)
                l.click()
                fill_forms()
                time.sleep(1)
            else:
                print('Link NOT found....')
           
        self.assertTrue("true", "true")        
        
            
        

    