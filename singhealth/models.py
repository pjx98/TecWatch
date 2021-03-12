from django.db import models
from django.utils import timezone

# Create your models here.
class Staff(models.Model):
    name = models.CharField(max_length = 100, null=True)
    username = models.CharField(max_length = 100, null=True)
    email = models.CharField(max_length = 100, null=True)
    date_created = models.DateTimeField(default = timezone.now, null=True)

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
    date_created = models.DateTimeField(default = timezone.now, null=True)
    outlet = models.ForeignKey(Outlet, null=True, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

class Complaint(models.Model):
    STATUS = (
        ('Open', 'Open'),
        ('Expired', 'Expired'),
        ('Resolved', 'Resolved'),
    )
    
    subject = models.CharField(max_length = 100, null=True)
    score = models.PositiveIntegerField(null = True)
    deadline = models.DateField(help_text="YYYY-MM-DD", null=True)
    date_created = models.DateTimeField(default = timezone.now, null=True)
    notes = models.TextField(null=True, help_text = "**Not visible to tenant")
    status = models.CharField(max_length = 100, null=True, choices = STATUS)
    
    staff = models.ForeignKey(Staff, null=True, on_delete = models.CASCADE)
    tenant = models.ForeignKey(Tenant, null=True, on_delete = models.CASCADE)

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
    
    

    
        




