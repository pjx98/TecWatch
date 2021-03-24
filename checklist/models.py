from django.db import models

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
    
    score = models.PositiveIntegerField(null = True)
    complaint = models.OneToOneField("singhealth.Complaint", null=True, on_delete = models.CASCADE, related_name='score')
    checked = models.ManyToManyField(ChecklistItem, related_name='checked')
    

    
    
    

    
