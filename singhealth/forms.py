from django import forms
from .models import Complaint

#DataFlair #File_Upload
class Complaint_Form(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
        'title',
        'score',
        'picture',
        'deadline',
        'suggestions',
        'notes',
        ]
        




"""Model Forms: derive structure from models
when making a form using ModelForm class, use META class"""