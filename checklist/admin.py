from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ChecklistItem)
admin.site.register(Checklist)
admin.site.register(ChecklistScore)
