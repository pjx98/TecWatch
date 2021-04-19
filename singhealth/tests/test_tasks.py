from notification.tasks import *
from django.core import mail
from datetime import date
import time
from django.test.utils import override_settings    
from django.test import TestCase
from django.contrib.auth.models import User, Group
from singhealth.models import Complaint
from checklist.models import *
from notification.tasks import *
from background_task.tasks import tasks
from background_task.models import Task

# python manage.py test singhealth.tests.test_tasks.EmailTest


class EmailTest(TestCase):
    def setUp(self):
        #create users
        staff_group = Group.objects.create(name='Staff')
        tenant_group = Group.objects.create(name='Tenant')
        staff = User.objects.create_superuser(
            username = 'staff', 
            password = '~1qaz2wsx', 
            email = "staff@gmail.com")
        staff.set_password('~1qaz2wsx')
        staff.groups.add(staff_group)    
        tenant = User.objects.create_superuser(
            username = 'tenant', 
            password = '~1qaz2wsx', 
            email = "tenant@gmail.com")
        tenant.set_password('~1qaz2wsx')
        tenant.groups.add(tenant_group)    
        staff.save()
        tenant.save()
        
        #create checklist items
        item1 = ChecklistItem.objects.create(description = "Professionalism")
        item2 = ChecklistItem.objects.create(description = "Food Hygiene")
        item3 = ChecklistItem.objects.create(description = "Safety")
        item1.save()
        item2.save()
        item3.save()
        
        #create empty checklists
        fnbchecklist = Checklist.objects.create(category='fnb')
        fnbchecklist.items.add(item1, item2)
        fnbchecklist.save()
        
        nonfnbchecklist = Checklist.objects.create(category='nonfnb')
        nonfnbchecklist.items.add(item1, item3)
        nonfnbchecklist.save()     
        
        
        #create audit record 
        audit = ChecklistScore.objects.create(
            score = 1, 
            tenant = tenant,
            checked = ["Professionalism"],
            unchecked = ["Food Hygiene"])
        audit.save()
        
            
        

    # python manage.py test notification.tests.test_tasks.EmailTest.test_send_notification_tenant
    def test_send_notification_tenant(self):
        #create open complaint
        deadline = date(2021, 12, 12)
        staff = User.objects.get(username='staff')
        tenant = User.objects.get(username='tenant')
        audit = ChecklistScore.objects.get(tenant = tenant)
        
        complaint = Complaint.objects.create(
            subject = "Test", 
            deadline = deadline, 
            notes = "testing notes", 
            status = "Open", 
            staff = staff,
            tenant = tenant, 
            checklist = audit)
        complaint.save() 
        
        Task.objects.all().delete()
        send_notification()
        tasks.run_next_task()
        time.sleep(1)
        assert len(mail.outbox) == 1, len(mail.outbox)
        assert mail.outbox[0].subject == "Notification on Unresolved Complaints", mail.outbox[0].subject
        assert mail.outbox[0].body == "Dear tenant,\n\nYou have 1 unresolved complaints. \n\nPlease log onto the Singhealth retail management app to submit your rectification. \n\nThank you.", mail.outbox[0].body
        assert mail.outbox[0].to == ['tenant@gmail.com'], mail.outbox[0].to
        
    # python manage.py test notification.tests.test_tasks.EmailTest.test_send_notification_staff
    def test_send_notification_staff(self):
        #create expired complaint
        deadline = date(2021, 1, 1)
        staff = User.objects.get(username='staff')
        tenant = User.objects.get(username='tenant')
        audit = ChecklistScore.objects.get(tenant = tenant)
        
        complaint = Complaint.objects.create(
            subject = "Test", 
            deadline = deadline, 
            notes = "testing notes", 
            status = "Expired", 
            staff = staff,
            tenant = tenant, 
            checklist = audit)
        complaint.save() 
        
        Task.objects.all().delete()
        send_notification()
        tasks.run_next_task()
        time.sleep(1)
        assert len(mail.outbox) == 1, len(mail.outbox)
        assert mail.outbox[0].subject == "Notification on Expired Complaint", mail.outbox[0].subject
        assert mail.outbox[0].body == "Dear staff, \n\nThe complaint you had previously made against tenant has expired, and a rectification has not been made. \n\nYou may log onto the Singhealth retail management app to view the relevant details. \n\nThank you.", mail.outbox[0].body
        assert mail.outbox[0].to == ['staff@gmail.com'], mail.outbox[0].to
        
    # python manage.py test notification.tests.test_tasks.EmailTest.test_check_deadline
    def test_check_deadline(self):
        #create expired complaint
        deadline = date(2021, 1, 1)
        staff = User.objects.get(username='staff')
        tenant = User.objects.get(username='tenant')
        audit = ChecklistScore.objects.get(tenant = tenant)
        
        complaint = Complaint.objects.create(
            subject = "Test", 
            deadline = deadline, 
            notes = "testing notes", 
            status = "Open", 
            staff = staff,
            tenant = tenant, 
            checklist = audit)
        complaint.save()
        
        Task.objects.all().delete()
        check_deadline()
        tasks.run_next_task()
        time.sleep(1)
        
        complaint = Complaint.objects.get(subject="Test")
        assert complaint.status == "Expired", complaint.status
    
    # python manage.py test notification.tests.test_tasks.EmailTest.test_update_notification_resolved
    def test_update_notification_resolved(self):
        #create complaint
        deadline = date(2021, 12, 12)
        staff = User.objects.get(username='staff')
        tenant = User.objects.get(username='tenant')
        audit = ChecklistScore.objects.get(tenant = tenant)
        
        complaint = Complaint.objects.create(
            subject = "Test", 
            deadline = deadline, 
            notes = "testing notes", 
            status = "Open", 
            staff = staff,
            tenant = tenant, 
            checklist = audit)
        complaint.save()
        
        Task.objects.all().delete()
        update_notification("resolved", complaint.id)
        tasks.run_next_task()
        time.sleep(1)
        
        assert len(mail.outbox) == 1, len(mail.outbox)
        assert mail.outbox[0].subject == "Notification on Resolved Complaint", mail.outbox[0].subject
        assert mail.outbox[0].body == "Dear tenant, \n\nA complaint with subject: Test has been resolved. \n\nThank you for your timely rectification.", mail.outbox[0].body
        assert mail.outbox[0].to == ['tenant@gmail.com'], mail.outbox[0].to
        
        
    # python manage.py test notification.tests.test_tasks.EmailTest.test_update_notification_rectification
    def test_update_notification_rectification(self):
        #create complaint
        deadline = date(2021, 12, 12)
        staff = User.objects.get(username='staff')
        tenant = User.objects.get(username='tenant')
        audit = ChecklistScore.objects.get(tenant = tenant)
        
        complaint = Complaint.objects.create(
            subject = "Test", 
            deadline = deadline, 
            notes = "testing notes", 
            status = "Open", 
            staff = staff,
            tenant = tenant, 
            checklist = audit)
        complaint.save()
        
        Task.objects.all().delete()
        update_notification("rectification", complaint.id)
        tasks.run_next_task()
        time.sleep(1)
        
        assert len(mail.outbox) == 1, len(mail.outbox)
        assert mail.outbox[0].subject == "Notification on Uploaded Rectification", mail.outbox[0].subject
        assert mail.outbox[0].body == "Dear staff, \n\ntenant has uploaded a rectification for complaint with subject: Test. \n\nYou may log onto the Singhealth retail management app to view the rectification details. \n\nThank you.", mail.outbox[0].body
        assert mail.outbox[0].to == ['staff@gmail.com'], mail.outbox[0].to
        
        
    