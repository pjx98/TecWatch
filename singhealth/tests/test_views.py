from django.test import TestCase
from django.utils import timezone
import datetime
from django.contrib.auth.models import User, Group
from singhealth.models import Complaint
from singhealth.views import *
from django.urls import reverse
from django.test.client import Client

# python manage.py test singhealth.tests.test_views.loginInRequired
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
        
    def test_login_required_staff_homepage(self):
        response = self.client.get(reverse("homestaff"))
        self.assertRedirects(response, '/singhealth/?next=/singhealth/homestaff/')
        
    def test_login_required_tenant_homepage(self):
        response = self.client.get(reverse("hometenant"))
        self.assertRedirects(response, '/singhealth/?next=/singhealth/hometenant/')
        
    def test_invalid_login(self):
        login = self.client.login(username='invalid', password='invalid')
        
        # invalid login should remain in login page
        response = self.client.get(reverse('login'))
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
                                                       score=5,
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
        response = self.client.post(reverse('view_complaint'),data={"complaintId": 1})
        
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
        response = self.client.post(reverse('view_complaint'),data={"complaintId": 1})
        
        # Check if tenant is logged in
        self.assertEqual(str(response.context['user']), 'tenant')
        # Check for response 'success'
        self.assertEqual(response.status_code, 200)
        
        # Check if correct template is used
        self.assertTemplateUsed(response, 'view_complaint.html')
        
        #check tenant action field 
        action_field = (response.context['action'])
        self.assertEqual("Upload Rectification", action_field)
        
        
        
        
        