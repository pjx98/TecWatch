from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Outlet(models.Model):
    TYPE = (
        ('F & B', 'F & B'),
        ('Others', 'Others'),
    )

    LOCATION = (
        ('West', 'West'),
        ('East', 'East'),
        ('North', 'North'),
        ('South', 'South'),
    )

    type = models.CharField(max_length = 100, null=True, choices=TYPE)
    location = models.CharField(max_length=100, null=True, choices=LOCATION)

    def __str__(self):
        return self.location + " (" + self.type + ")"


class Complaint(models.Model):
    STATUS = (
        ('Editing', 'Editing'),
        ('Open', 'Open'),
        ('Expired', 'Expired'),
        ('Resolved', 'Resolved'),
    )
    
    subject = models.CharField(max_length = 100, null=True)
    deadline = models.DateField(help_text="YYYY-MM-DD", null=True)
    date_created = models.DateTimeField(default = timezone.now, null=True)
    notes = models.TextField(null=True, help_text = "**Not visible to tenant")
    status = models.CharField(max_length = 100, null=True, choices = STATUS)
    staff = models.ForeignKey(User, null=True, on_delete = models.CASCADE, related_name='staff')
    checklist = models.ForeignKey("checklist.ChecklistScore", null=True, on_delete = models.CASCADE)
    
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete = models.CASCADE, related_name='tenant_complaint')

    def __str__(self):
        return str(self.id)
    
    
class Update(models.Model):
    subject = models.CharField(max_length = 100, null=True)
    date = models.DateTimeField(default = timezone.now, null=True)
    comments = models.TextField(null=True)
    photo = models.ImageField(null=True)
    complaint = models.ForeignKey(Complaint, null=True, on_delete = models.CASCADE)
    edit_name = models.CharField(max_length = 100, null=True)
    
    def __str__(self):
        return "response to complaint " + str(self.complaint.id)
    
    

    
        




