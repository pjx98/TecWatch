from django.shortcuts import render, redirect
from .forms import AddItemForm, CheckboxForm, ScoreForm
from .models import ChecklistItem, Checklist, ChecklistScore
from django.forms import modelformset_factory


from django.contrib.auth import authenticate, login, logout, get_user_model

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *

from .decorators import *

@login_required(login_url='login')
@allowed_users(allowed_roles=['Staff'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['Staff'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['Staff'])
def fnb(request):
    context = {}
    
    checklist = Checklist.objects.get(category = "fnb")
    items = checklist.items.all()
    form = CheckboxForm(instance=checklist)
    
    context['items'] = items
    context['category'] = "fnb"
    context['form'] = form
    return render(request, 'view_checklist.html', context)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['Staff'])  
def nonfnb(request):
    context = {}
    checklist = Checklist.objects.get(category = "nonfnb")
    items = checklist.items.all()
    form = CheckboxForm(instance=checklist)
    
    context['items'] = items
    context['category'] = "nonfnb"
    context['form'] = form
    return render(request, 'view_checklist.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Staff'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['Staff'])
def audit(request):
    context = {}
    
    if request.method == "POST":
        tenantId = request.POST.get('tenantId', -1)
        tenant = User.objects.get(username=tenantId)
        category = request.POST.get('checklist', 0)
        checklist = Checklist.objects.get(category = category) 
        formc = ScoreForm(category = category)
        context['form'] = formc
        context['category'] = category 
        context['tenant'] = tenant
        
            
    elif request.method == "GET":
        tenantId = request.GET.get('tenantId', -1)
        tenant = User.objects.get(username=tenantId)
            
    context['tenant'] = tenant
    return render(request, 'audit.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Staff'])
def view_audit(request):
    context = {}
    
    if request.method == "POST":
        tenantId = request.POST.get('audit', -1)
    elif request.method == "GET":
        tenantId = request.GET.get('audit', -1)  
        
    tenant = User.objects.get(username=tenantId)
    audits = ChecklistScore.objects.filter(tenant = tenant).order_by('date_created')[::-1]
    context['audits'] = audits
    context['tenant'] = tenant
    return render(request, 'view_audit.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Staff'])
def calculate_score(request):
    context = {}
    
    category = request.POST.get('category', 0)
    checklist = Checklist.objects.get(category = category) 
    
    tenantId = request.POST.get('tenantId', -1)
    tenant = User.objects.get(username=tenantId)
    
    formc = ScoreForm(category = category)
    form = ScoreForm(request.POST, request.FILES, category = category)
    if form.is_valid():
        checked = form.cleaned_data['items']
        score = checked.count()
        score_object = ChecklistScore(score = score)
        score_object.save()
        score_object.checked = list(checked.values_list('description', flat=True))
                
        score_object.unchecked = list(set(formc.fields['items'].queryset.values_list('description', flat=True)) - set(score_object.checked))
        score_object.tenant = tenant
        score_object.save()
        context['score'] = score
        context['checked'] = score_object.checked
        context['test'] = score_object.unchecked
        
    return redirect('/singhealth/homestaff')
    
    
    
    

    