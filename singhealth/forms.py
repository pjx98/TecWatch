from django import forms
from .models import Complaint

#DataFlair #File_Upload
class Complaint_Form(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [            
        'tenant',
        'subject',
        'score',
        'picture',
        'deadline',
        'suggestions',
        'notes',
        ]

        
        
class Rectification_Form(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
        'tenant_response',
        'tenant_picture',
        ]
        
        labels = {
            'tenant_response' : "Your response",
            'tenant_picture' : "Upload picture"
        }
        
        



"""Model Forms: derive structure from models
when making a form using ModelForm class, use META class

widgets = {'name': forms.HiddenInput()}"""