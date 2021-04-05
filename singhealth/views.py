from django.shortcuts import render, redirect
from .forms import Complaint_Form, Update_Form, Complaint_Tenant, Complaint_Notes
from .models import Complaint, Outlet, Update
from django.utils import timezone
from checklist.models import ChecklistScore

from django.shortcuts import get_object_or_404

from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout, get_user_model

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import  CreateUserForm

from .decorators import *

from notification.tasks import update_notification

# Create your views here.
def home(request):
    return HttpResponse('Home Page')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Staff'])
def create_complaint(request):
    context = {}
    
    if request.method == 'POST':
       
        form1 = Complaint_Tenant(request.POST, request.FILES)
        form2 = Complaint_Form(request.POST, request.FILES)
        form3 = Update_Form(request.POST, request.FILES)            
            
        if form1.is_valid() and form2.is_valid():      
        
            complaint = form2.save(commit=False)
            complaint.tenant = form1.cleaned_data['tenant']
            complaint.status = 'Open'
            complaint.staff = request.user
            complaint.checklist = form1.cleaned_data['checklist']
            
            if form3.is_valid():
                update = form3.save(commit=False)
                update.complaint = complaint
                update.edit_name = str(complaint.staff.username)
                complaint.subject = update.subject
                complaint.deadline = request.POST.get('deadline', 0)
                
                complaint.save()
                update.save() 
                
                return redirect('homestaff')
            
    context['staff'] = request.user
            
    form1 = Complaint_Tenant()
    context['form_complaint1'] = form1
    form2 = Update_Form()
    context['form_update'] = form2    
    form3 = Complaint_Form()
    context['form_complaint2'] = form3
            
    return render(request, 'create.html', context)
            



@login_required(login_url='login')
@allowed_users(allowed_roles=['Staff'])
def homestaff(request):
    context = {}
    identity = request.user.groups.all()[0].name
    staff = request.user
    
    complaints = Complaint.objects.filter(staff = staff).order_by('date_created')[::-1]

    username = request.user.username
    User = get_user_model()
    tenants = User.objects.filter(groups__name='Tenant')

    context['staff'] = username
    context['tenants'] = tenants
    context['complaints'] = complaints

    
    return render(request, 'home_staff.html', context)    
    
    
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['Tenant'])
def hometenant(request):
    context = {}
    
    tenant = request.user
    #loginId = request.POST.get('loginId', 0)
    #tenant = Tenant.objects.get(username = loginId)
    context['tenant'] = tenant
    complaints = Complaint.objects.filter(tenant = tenant).order_by('date_created')[::-1]
    context['complaints'] = complaints
    return render(request, 'home_tenant.html', context)    

    return render(request, 'error.html')



@login_required(login_url='login')
@allowed_users(allowed_roles=['Staff'])
def view_tenant(request):
    if request.method == "POST":
        context = {}
        username = request.user.username
        User = get_user_model()
        #get username of tenant
        tenantId = request.POST.get('complaint', -1)
        tenant = User.objects.get(username=tenantId)

        #to change to filter out complaint against specific tenant
        complaints = Complaint.objects.filter(tenant = tenant).order_by('date_created')[::-1]

        context['tenant'] = tenant
        context['complaints'] = complaints
        context['staff'] = request.user
        return render(request, 'view_tenant.html', context)
        
        
    
@login_required(login_url='login')
def view_complaint(request):
    if request.method == "POST":
        context = {}
        try:
            identity = request.user.groups.all()[0].name
            complaintId = request.POST.get('complaintId', -1)
            complaint = Complaint.objects.get(id = complaintId)
            if identity == "Staff":
                action = "Upload more details"
            elif identity == "Tenant":
                action = "Upload Rectification"            
            context['action'] = action
            
        except:
            complaintid = request.POST.get('resolveid', -1)
            complaint = Complaint.objects.get(id = complaintid)  
            complaint.status = 'Resolved' 
            complaint.save()
            update_notification("resolved", complaintid)
            
        #context['action'] = action
        updates = Update.objects.filter(complaint = complaint)
        context['updates'] = updates
        context['complaint'] = complaint
        context['identity'] = identity
        return render(request, 'view_complaint.html', context)
            
        
    return render(request, 'error.html')


@login_required(login_url='login')
def update(request):
    if request.method == "POST":
        context = {}
        
        identity = request.user.groups.all()[0].name
        complaintId = request.POST.get('updateid', -1)
        complaint = Complaint.objects.get(id = complaintId)
        form1 = Update_Form()
        updates = Update.objects.filter(complaint = complaint)
        
  
        if identity == "Staff":
            form2 = Complaint_Notes()
            context['form_notes'] = form2
            title = "Update Complaint"
        
        elif identity == "Tenant":
            title = "Upload Rectification"

        context['identity'] = identity
        context['complaint'] = complaint
        context['form_update'] = form1
        context['updates'] = updates
        context['title'] = title
        
            
        return render(request, 'update.html', context)
    
    return render(request, 'error.html')

@login_required(login_url='login')
def update_success(request):
    if request.method =="POST":
        identity = request.user.groups.all()[0].name
        complaintId = request.POST.get('comId', -1)
        complaint = Complaint.objects.get(id=complaintId)
        update = Update_Form(request.POST, request.FILES)
        if update.is_valid():
            u = update.save(commit = False)
            u.complaint = complaint
        else: 
            return render(request, 'error.html')
        
        if identity == "Staff":
            action = "Update"
            userId = complaint.staff.username
            u.edit_name = complaint.staff.username
            u.save()
            notes = Complaint_Notes(request.POST, request.FILES)
            if notes.is_valid():
                n = notes.save(commit = False)
                complaint.notes += "\n" + n.notes
                complaint.save()
                return redirect('/singhealth/successstaff')
            
        elif identity == "Tenant":
            action = "Rectification"
            userId = complaint.tenant.username
            u.edit_name = complaint.tenant.username
            u.save()
            update_notification("rectification", complaintId)
            return redirect('/singhealth/successtenant')
            
    
    return render(request, 'error.html')

@login_required(login_url='login')
def success_staff(request):
    context = {}
    update = Update.objects.order_by('date')[::-1][0]
    userId = update.complaint.staff.username
    context['userId'] = userId
    context['action'] = "Update"
    context['identity'] = request.user.groups.all()[0].name
    return render(request, 'success.html', context)

@login_required(login_url='login')
def success_tenant(request):
    context = {}
    update = Update.objects.order_by('date')[::-1][0]
    userId = update.complaint.tenant.username
    context['userId'] = userId
    context['action'] = "Rectification"
    context['identity'] = request.user.groups.all()[0].name
    return render(request, 'success.html', context)
    

def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='tenant')
			user.groups.add(group)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'register.html', context)


def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			if user.groups.filter (name="Staff"):
				return redirect('homestaff')
			elif user.groups.filter (name='Tenant'):
				return redirect('hometenant')

            
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Staff'])
def staff(request):
	return render(request, 'staff.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Tenant'])
def tenant(request):
	return render(request, 'tenant.html')
