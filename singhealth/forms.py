from django import forms
from .models import Complaint, Update

#DataFlair #File_Upload
class Complaint_Form(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [     
        'score',
        'deadline',
        'notes',
        ]

        

        
class Update_Form(forms.ModelForm):
    class Meta:
        model = Update
        fields = [
            'subject',
            'photo',
            'comments',
            
        ]
        
        labels = {
            'photo' : "Upload picture"
        }
        
        
class Complaint_Tenant(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'tenant',
        ]
        
class Complaint_Notes(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'notes'
        ]
        



"""Model Forms: derive structure from models
when making a form using ModelForm class, use META class

widgets = {'name': forms.HiddenInput()}"""