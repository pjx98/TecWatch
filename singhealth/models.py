from django.db import models
from django.utils import timezone

# Create your models here.
class Staff(models.Model):
    name = models.CharField(max_length = 100, null=True)
    username = models.CharField(max_length = 100, null=True)
    email = models.CharField(max_length = 100, null=True)
    date_created = models.DateTimeField(auto_now_add = True, null=True)

    def __str__(self):
        return self.name

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

class Tenant(models.Model):
    name = models.CharField(max_length = 100, null=True)
    username = models.CharField(max_length = 100, null=True)
    email = models.CharField(max_length = 100, null=True)
    date_created = models.DateTimeField(auto_now_add = True, null=True)
    outlet = models.ForeignKey(Outlet, null=True, on_delete = models.SET_NULL)

    def __str__(self):
        return self.name

class Complaint(models.Model):
    STATUS = (
        ('Pending Tenant Response', 'Pending Tenant Response'), 
        ('Pending Staff Response', 'Pending Staff Response'),
        ('Resolved', 'Resolved'),
    )
    
    
    subject = models.CharField(max_length = 100, null=True)
    date_created = models.DateTimeField(default= timezone.now, null=True)
    score = models.PositiveIntegerField(null = True)
    picture = models.ImageField(null=True)
    deadline = models.DateField(help_text="YYYY-MM-DD", null=True)
    suggestions = models.TextField(null=True, help_text ="**Shown to tenant")
    notes = models.TextField(null=True, help_text = "**Not visible to tenant")
    tenant_response = models.TextField(null=True, default= "")
    tenant_picture = models.ImageField(null=True)
    status = models.CharField(max_length = 100, null=True, choices = STATUS)
    
    

    staff = models.ForeignKey(Staff, null=True, on_delete = models.SET_NULL)
    tenant = models.ForeignKey(Tenant, null=True, on_delete = models.SET_NULL)

    def __str__(self):
        return self.subject + " created on " + str(self.date_created)
    

    
        




