from django import forms
from .models import Complaint, Update
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

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
        
        
# class Complaint_Tenant(forms.ModelForm):
#     class Meta:
#         model = Complaint
#         fields = [
#             'tenant',
#         ]

class Complaint_Tenant(forms.Form):
        tenant = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Tenant'))
        
class Complaint_Notes(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'notes'
        ]
        

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']





"""Model Forms: derive structure from models
when making a form using ModelForm class, use META class

widgets = {'name': forms.HiddenInput()}"""