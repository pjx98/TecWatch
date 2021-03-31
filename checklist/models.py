from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField


# Create your models here.
    

    
class ChecklistItem(models.Model):
    
    description = models.CharField(max_length = 200, null=True, default = "no description")
    box = models.BooleanField(blank = True, default = False)
    
    def __str__(self):
        return self.description
    
class Checklist(models.Model):
    CATEGORY = (
        ('fnb', 'fnb'),
        ('nonfnb', 'nonfnb'),
    )
    
    category = models.CharField(max_length = 10, null = True, choices = CATEGORY, default = "no category")
    items = models.ManyToManyField(ChecklistItem, related_name='checklist')
    
    def __str__(self):
        return self.category
    
class ChecklistScore(models.Model):
    
    date_created = models.DateTimeField(default=timezone.now, null=True)
    score = models.PositiveIntegerField(null = True)
    checked = PickledObjectField(default = dict)
    unchecked = PickledObjectField(default = dict)
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete = models.CASCADE, related_name='tenant_checklist')
    
    def __str__(self):
        return str(self.date_created)[:10] + "; Score: " + str(self.score) + " (" + str(self.tenant.username) + ")" 
    
    
    

    
    
    

    
