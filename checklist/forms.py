from django import forms
from .models import ChecklistItem, Checklist, ChecklistScore
from django.utils.translation import gettext_lazy as _

class AddItemForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = [
            'description',
        ]
        
        
        
        
class CheckboxForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ['items']
        
    items = forms.ModelMultipleChoiceField(
        queryset = ChecklistItem.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        label = ""
    )

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ['items']
        
    
    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category')
        super().__init__(*args, **kwargs)
        if category:
            self.fields['items'] = forms.ModelMultipleChoiceField(
                queryset = Checklist.objects.get(category=category).items.all(),
                widget = forms.CheckboxSelectMultiple,
                label = "",
            )   
    
    
        
        
        