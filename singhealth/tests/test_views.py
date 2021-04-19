from django.test import TestCase
from django.utils import timezone
import datetime
from django.contrib.auth.models import User, Group
from singhealth.models import Complaint
from singhealth.views import *
from django.urls import reverse
from django.test.client import Client
import random
from django.contrib.auth import authenticate
from django.http import HttpRequest
from django.core import mail

from importlib import import_module

from django.contrib.auth import get_user_model, login, logout
from django.http import HttpRequest
from django.test import override_settings, TestCase
from django.urls import reverse

# python manage.py test singhealth.tests.test_views

# python manage.py test singhealth.tests.test_views.loginInRequired
@override_settings(AXES_ENABLED=False)
class loginInRequired(TestCase):
    
    def setUp(self):
        
        # Create Staff and Tenant user
        staff_group = Group.objects.create(name='Staff')
        tenant_group = Group.objects.create(name='Tenant')
    
        staff = User.objects.create_superuser(username = 'staff', password = '~1qaz2wsx')
        staff.set_password('~1qaz2wsx')
        staff.groups.add(staff_group)
    
        tenant = User.objects.create_superuser(username = 'tenant', password = '~1qaz2wsx')
        tenant.set_password('~1qaz2wsx')
        tenant.groups.add(tenant_group)
    
        staff.save()
        tenant.save()
        
        #self.user.backend = "django.contrib.auth.backends.ModelBackend"
        
    # Test login_required decorator
    def test_login_required_staff_homepage(self):
        response = self.client.get(reverse("homestaff"))
        self.assertRedirects(response, '/singhealth/?next=/singhealth/homestaff/')
    
    #Test login_required decorator
    def test_login_required_tenant_homepage(self):
        response = self.client.get(reverse("hometenant"))
        self.assertRedirects(response, '/singhealth/?next=/singhealth/hometenant/')
        
    def test_login_with_invalid_and_valid(self):
        login = self.client.login(username='invalid', password='invalid')
        
        # invalid login should remain in login page
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
        login = self.client.login(username='', password='invalid')
        
        # invalid login should remain in login page
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
        login = self.client.login(username='invalid', password='')
        
        # invalid login should remain in login page
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
        login = self.client.login(username='staff', password='~1qaz2wsx')
        
        # correct login
        response = self.client.get(reverse('homestaff'))
        self.assertEqual(response.status_code, 200)
        
        
        
        
        
    def test_logged_in_uses_correct_template(self):
        
        ######## Test for staff
        login = self.client.login(username='staff', password='~1qaz2wsx')
        response = self.client.get(reverse("homestaff"))
        
        # Check if staff is logged in
        self.assertEqual(str(response.context['user']), 'staff')
        # Check for response 'success'
        self.assertEqual(response.status_code, 200)
        # Check if correct template is used
        self.assertTemplateUsed(response, 'home_staff.html')
        
        
        ####### Test for tenant
        login = self.client.login(username='tenant', password='~1qaz2wsx')
        response = self.client.get(reverse("hometenant"))
        
        # Check if tenant is logged in
        self.assertEqual(str(response.context['user']), 'tenant')
        # Check for response 'success'
        self.assertEqual(response.status_code, 200)
        # Check if correct template is used
        self.assertTemplateUsed(response, 'home_tenant.html')
        
        
    

# python manage.py test singhealth.tests.test_views.PostMethod
@override_settings(AXES_ENABLED=False)
class PostMethod(TestCase):
    
    def setUp(self):
        
        # Create Staff and Tenant user
        staff_group = Group.objects.create(name='Staff')
        tenant_group = Group.objects.create(name='Tenant')
    
        staff = User.objects.create_superuser(username = 'staff', password = '~1qaz2wsx')
        staff.set_password('~1qaz2wsx')
        staff.groups.add(staff_group)
    
        tenant = User.objects.create_superuser(username = 'tenant', password = '~1qaz2wsx')
        tenant.set_password('~1qaz2wsx')
        tenant.groups.add(tenant_group)
    
        staff.save()
        tenant.save() 
        
        # Create complaint object
        test_complaint_form = Complaint.objects.create(status='Open',
                                                       subject='test_subject',
                                                       deadline='2020-04-12',
                                                       date_created='2020-04-01',
                                                       notes='test_notes',
                                                       staff=staff,
                                                       tenant=tenant,
                                                       )

        
        
    def test_view_complaint_staff(self):
        
        # staff login
        login = self.client.login(username='staff', password='~1qaz2wsx')
        
        # send in POST request
        response = self.client.post(reverse('viewcomplaint'),data={"complaintId": 1})
        
        # Check if staff is logged in
        self.assertEqual(str(response.context['user']), 'staff')
        # Check for response 'success'
        self.assertEqual(response.status_code, 200)
        
        # Check if correct template is used
        self.assertTemplateUsed(response, 'view_complaint.html')
        
        #check staff action field 
        action_field = (response.context['action'])
        self.assertEqual("Upload more details", action_field)
        
    def test_view_complaint_tenant(self):
        
        # staff login
        login = self.client.login(username='tenant', password='~1qaz2wsx')
        
        # send in POST request
        response = self.client.post(reverse('viewcomplaint'),data={"complaintId": 1})
        
        # Check if tenant is logged in
        self.assertEqual(str(response.context['user']), 'tenant')
        # Check for response 'success'
        self.assertEqual(response.status_code, 200)
        
        # Check if correct template is used
        self.assertTemplateUsed(response, 'view_complaint.html')
        
        #check tenant action field 
        action_field = (response.context['action'])
        self.assertEqual("Upload Rectification", action_field)

            
#python manage.py test singhealth.tests.test_views.EmailTest
class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail('Subject here', 'Here is the message.',
            'from@example.com', ['to@example.com'],
            fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject here')