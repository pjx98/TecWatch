from django.test import TestCase
from django.utils import timezone
import datetime
from django.contrib.auth.models import User, Group
from singhealth.models import Complaint

# python manage.py test singhealth.tests.test_models.ComplaintModelTest
class ComplaintModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Complaint.objects.create(
        subject = 'Test',
        deadline = "2021-03-31",
        notes = "notes",
        )
        
        staff_group = Group.objects.create(name='Staff')
        tenant_group = Group.objects.create(name='Tenant')
        
        staff = User.objects.create(username = 'staff', password = '~1qaz2wsx')
        staff.groups.add(staff_group)
        tenant = User.objects.create(username = 'tenant', password = '~1qaz2wsx')
        tenant.groups.add(tenant_group)
        
        
    def setUp(self):
        #"setUp: Run once for every test method to setup clean data."
        pass
    
    def test_subject_label(self):
        complaint = Complaint.objects.get(id=1)
        label = complaint._meta.get_field('subject').verbose_name
        self.assertEqual(label, 'subject')
    
    def test_deadline_label(self):
        complaint = Complaint.objects.get(id=1)
        label = complaint._meta.get_field('deadline').verbose_name
        self.assertEqual(label, 'deadline')
        
    def test_date_created_label(self):
        complaint = Complaint.objects.get(id=1)
        label = complaint._meta.get_field('date_created').verbose_name
        self.assertEqual(label, 'date created')
        
    def test_notes_label(self):
        complaint = Complaint.objects.get(id=1)
        label = complaint._meta.get_field('notes').verbose_name
        self.assertEqual(label, 'notes')
        
    def test_status_label(self):
        complaint = Complaint.objects.get(id=1)
        label = complaint._meta.get_field('status').verbose_name
        self.assertEqual(label, 'status')
        
        
    def test_staff_label(self):
        complaint = Complaint.objects.get(id=1)
        label = complaint._meta.get_field('staff').verbose_name
        self.assertEqual(label, 'staff')
        
    def test_tenant_label(self):
        complaint = Complaint.objects.get(id=1)
        label = complaint._meta.get_field('tenant').verbose_name
        self.assertEqual(label, 'tenant')
        
    def test_subject_max_length(self):
        complaint = Complaint.objects.get(id=1)
        max_length = complaint._meta.get_field('subject').max_length
        self.assertEqual(max_length, 100)
        
    def test_status_max_length(self):
        complaint = Complaint.objects.get(id=1)
        max_length = complaint._meta.get_field('status').max_length
        self.assertEqual(max_length, 100)
        
        
    def test_correct_date_created(self):
        complaint = Complaint.objects.get(id=1)
        date_created = complaint.date_created
        self.assertTrue(isinstance(date_created, datetime.datetime))        
        
        today_min = datetime.datetime.now()
        today_min = today_min - datetime.timedelta(hours = 1)
        today_min= timezone.make_aware(today_min)
        
        today_max = datetime.datetime.now()
        today_max = today_max + datetime.timedelta(hours = 1)
        today_max= timezone.make_aware(today_max)
        
        
        self.assertTrue(today_min < date_created)
        self.assertTrue(date_created < today_max)
        
        
        
    def test_str(self):
        complaint = Complaint.objects.get(id=1)
        self.assertEqual(str(complaint), '1')
        
        
# theres assertRedirects/ assertTemplateUsed too