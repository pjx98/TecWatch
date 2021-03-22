from django.shortcuts import render, redirect
from .forms import AddItemForm, CheckboxForm, ScoreForm
from .models import ChecklistItem, Checklist, ChecklistScore
from django.forms import modelformset_factory


# Create your views here.
def add_items(request):
    if request.method == "POST":
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            if ChecklistItem.objects.filter(description = item.description).count() == 0:
                item.save()
    
    context = {}
    items = ChecklistItem.objects.all()
    form = AddItemForm()
    form.fields['description'].initial = ""
    
    context['items'] = items
    context['form'] = form
    
    return render(request, 'add_item.html', context)

    
def checklist_home(request):
    if request.method == "POST":
        option = request.POST.get('option', 0)
        if option == "new":
            return redirect('/checklist/additems')
        elif option == "fnb":
            return redirect('/checklist/fnb')
        elif option == "nonfnb":
            return redirect('/checklist/nonfnb')
        elif option == "audit":
            return redirect('/checklist/calculate')
        
    return render(request, 'checklist_home.html')

def fnb(request):
    context = {}
    
    checklist = Checklist.objects.get(category = "fnb")
    items = checklist.items.all()
    form = CheckboxForm(instance=checklist)
    
    context['items'] = items
    context['category'] = "fnb"
    context['form'] = form
    return render(request, 'view_checklist.html', context)
    
    
def nonfnb(request):
    context = {}
    checklist = Checklist.objects.get(category = "nonfnb")
    items = checklist.items.all()
    form = CheckboxForm(instance=checklist)
    
    context['items'] = items
    context['category'] = "nonfnb"
    context['form'] = form
    return render(request, 'view_checklist.html', context)

def update_checklist(request):
    context = {}
    if request.method == "POST":
        category = request.POST.get('category', 0)
        checklist = Checklist.objects.get(category = category)        
        form = CheckboxForm(request.POST,instance=checklist)
    
        if form.is_valid():
            form.save()
        
        if category == "fnb":
            return redirect('/checklist/fnb')
        
        elif category == "nonfnb":
            return redirect('/checklist/nonfnb')
    
    return render(request, 'view_checklist.html', context)


def calculate(request):
    context = {}
    if request.method == "POST":
        try:
            category = request.POST.get('checklist', 0)
            checklist = Checklist.objects.get(category = category) 
            form = ScoreForm(category=category)
            context['form'] = form
            context['category'] = category
            
        except:
            category = request.POST.get('category', 0)
            checklist = Checklist.objects.get(category = category) 
            form = ScoreForm(request.POST, request.FILES, category = category)
            if form.is_valid():
                checked = form.cleaned_data['items']
                score = checked.count()
                score_object = ChecklistScore(score = score)
                score_object.checked_set = checked
                score_object.save()
                context['score'] = score
                
                
            form = ScoreForm(category = category)
            context['form'] = form
            context['category'] = category              
            
    
    return render(request, 'calculate.html', context)

    