from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import Complaint_Form, Update_Form, Complaint_Tenant, Complaint_Notes
from .models import Complaint, Tenant, Staff, Outlet, Update
from django.utils import timezone

from .serializer import ComplaintSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    return HttpResponse('Home Page')

def create_complaint(request):
    
    if request.method == 'POST':
        context = {}
        try:    
            staffId = request.POST.get('staffId', -1)
            staff = Staff.objects.get(username = staffId)
            context['staff'] = staff
            
            form1 = Complaint_Tenant()
            context['form_complaint1'] = form1
            form2 = Update_Form()
            context['form_update'] = form2    
            form3 = Complaint_Form()
            context['form_complaint2'] = form3
            return render(request, 'create.html', context)
            
        except:    
            form1 = Complaint_Tenant(request.POST, request.FILES)
            form2 = Complaint_Form(request.POST, request.FILES)
            form3 = Update_Form(request.POST, request.FILES)
            if form1.is_valid() and form2.is_valid():
                complaint = form2.save(commit=False)
                complaint1 = form1.save(commit=False)
                complaint.tenant = complaint1.tenant
                complaint.status = 'Open'
                staffUsername = request.POST.get('userId', -1)
                complaint.staff = Staff.objects.get(username = staffUsername)
                if form3.is_valid():
                    update = form3.save(commit=False)
                    update.complaint = complaint
                    update.edit_name = complaint.staff.name
                    complaint.subject = update.subject
                    complaint.save()
                    update.save() 
                    
                    return redirect('/singhealth/success')
                
            
    return render(request, 'error.html')

def create_success(request):
    context = {}
    complaint = Complaint.objects.last()
    context['complaint'] = complaint
    update = Update.objects.get(complaint = complaint)
    context['update'] = update
    return render(request, 'complaint_success.html', context)

def login(request):
    return render(request, 'login_buttons.html')

def homestaff(request):
    context = {}
    if request.method == 'POST':
        loginId = request.POST.get('loginId', -1)
        staff = Staff.objects.get(username = loginId)
            
        context['staff'] = staff    
        tenants = Tenant.objects.all()
        context['tenants'] = tenants
        complaints = Complaint.objects.filter(staff = staff).order_by('date_created')[::-1]
        context['complaints'] = complaints
        
        return render(request, 'home_staff.html', context)    
    
    return render(request, 'error.html')
    
    
def hometenant(request):
    context = {}
    if request.method == 'POST':
        try:
            complaintid = request.POST.get('complaintid', -1)
            complaint = Complaint.objects.get(id = complaintid)  
            form = Rectification_Form()
            return render(request, 'rectify.html', {'complaint' : complaint, 'form': form})
        
        except: 
            loginId = request.POST.get('loginId', 0)
            tenant = Tenant.objects.get(username = loginId)
            context['tenant'] = tenant
            complaints = Complaint.objects.filter(tenant = tenant).order_by('date_created')[::-1]
            context['complaints'] = complaints
            return render(request, 'home_tenant.html', context)    
    
    return render(request, 'error.html')

def get_complaint_list(request):
    if request.method =="GET":
        complaint_list = Complaint.objects.all()
        serializer = ComplaintSerializer(complaint_list, many=True)
        return JsonResponse(serializer.data, safe=False)


def view_tenant(request):
    if request.method == "POST":
        context = {}
        tenantId = request.POST.get('tenantId', -1)
        staffId = request.POST.get('staffId', -1)
        tenant = Tenant.objects.get(username = tenantId)
        staff = Staff.objects.get(username = staffId)
        complaints = Complaint.objects.filter(staff = staff, tenant = tenant).order_by('date_created')[::-1]
        
        context['tenant'] = tenant
        context['complaints'] = complaints
        context['staff'] = staff
        return render(request, 'view_tenant.html', context)
        
    

def view_complaint(request):
    if request.method == "POST":
        context = {}
        
        
        try:
            complaintId = request.POST.get('complaintId', -1)
            complaint = Complaint.objects.get(id = complaintId)
            identity = request.POST.get('identity', 0)
            if identity == "staff":
                action = "Upload more details"
            elif identity == "tenant":
                action = "Upload Rectification"            
            context['action'] = action
            
       
        except:
            
            complaintid = request.POST.get('resolveid', -1)
            complaint = Complaint.objects.get(id = complaintid)  
            complaint.status = 'Resolved' 
            complaint.save()
            identity = "staff"
            
        
        updates = Update.objects.filter(complaint = complaint)
        context['updates'] = updates
        context['complaint'] = complaint
        context['identity'] = identity
        return render(request, 'view_complaint.html', context)
            
        
    return render(request, 'error.html')

def update(request):
    if request.method == "POST":
        context = {}
        identity = request.POST.get('identity', 0)
        complaintId = request.POST.get('updateid', -1)
        complaint = Complaint.objects.get(id = complaintId)
        form1 = Update_Form()
        updates = Update.objects.filter(complaint = complaint)
        
        
        if identity == "staff":
            form2 = Complaint_Notes()
            context['form_notes'] = form2
            title = "Update Complaint"
        
        elif identity == "tenant":
            title = "Upload Rectification"

        context['identity'] = identity
        context['complaint'] = complaint
        context['form_update'] = form1
        context['updates'] = updates
        context['title'] = title
        
            
        return render(request, 'update.html', context)
    
    return render(request, 'error.html')

def update_success(request):
    if request.method =="POST":
        complaintId = request.POST.get('comId', -1)
        complaint = Complaint.objects.get(id=complaintId)
        update = Update_Form(request.POST, request.FILES)
        if update.is_valid():
            u = update.save(commit = False)
            u.complaint = complaint
        else: 
            return render(request, 'error.html')
        
        identity = request.POST.get('identity', 0)
        
        
        if identity == "staff":
            action = "Update"
            userId = complaint.staff.username
            u.edit_name = complaint.staff.name
            u.save()
            notes = Complaint_Notes(request.POST, request.FILES)
            if notes.is_valid():
                n = notes.save(commit = False)
                complaint.notes += "\n" + n.notes
                complaint.save()
                return redirect('/singhealth/successstaff')
            
        elif identity == "tenant":
            action = "Rectification"
            userId = complaint.tenant.username
            u.edit_name = complaint.tenant.name
            u.save()
            return redirect('/singhealth/successtenant')
            
    
    return render(request, 'error.html')

def success_staff(request):
    context = {}
    update = Update.objects.order_by('date')[::-1][0]
    userId = update.complaint.staff.username
    context['userId'] = userId
    context['action'] = "Update"
    context['identity'] = "staff"
    return render(request, 'success.html', context)

def success_tenant(request):
    context = {}
    update = Update.objects.order_by('date')[::-1][0]
    userId = update.complaint.tenant.username
    context['userId'] = userId
    context['action'] = "Rectification"
    context['identity'] = "tenant"
    return render(request, 'success.html', context)
    





