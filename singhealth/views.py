from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import Complaint_Form, Rectification_Form
from .models import Complaint, Tenant, Staff, Outlet
from .serializer import ComplaintSerializer
from django.utils import timezone

# Create your views here.
def home(request):
    return HttpResponse('Home Page')

def create_complaint(request):
    
    if request.method == 'POST':
        try:         
            form = Complaint_Form()
            staffId = request.POST.get('staffid', -1)
            staff = Staff.objects.get(username = staffId)
            return render(request, 'create.html', {'staff': staff, 'form': form})
            
        except:    
            form = Complaint_Form(request.POST, request.FILES)
            if form.is_valid():
                complaint = form.save(commit=False)
                complaint.status = 'Pending Tenant Response'
                staffUsername = request.POST.get('staffUsername', -1)
                complaint.staff = Staff.objects.get(username = staffUsername)
                complaint.save()
                return redirect('/singhealth/success')
    return render(request, 'error.html')

def create_success(request):
    complaint = Complaint.objects.last()
    return render(request, 'complaint_success.html', {'complaint': complaint,})

def login(request):
    return render(request, 'login_buttons.html')

def homestaff(request):
    context = {}
    if request.method == 'POST':
        try:
            complaintid = request.POST.get('resolveid', -1)
            complaint = Complaint.objects.get(id = complaintid)  
            complaint.status = 'Resolved' 
            complaint.save()
            staff = complaint.staff
            
        except:
            loginId = request.POST.get('loginId', 0)
            staff = Staff.objects.get(username = loginId)
            
        context['staff'] = staff    
        tenants = Tenant.objects.all()
        context['tenants'] = tenants
        complaints = Complaint.objects.filter(staff = staff)
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
            complaints = Complaint.objects.filter(tenant = tenant)
            context['complaints'] = complaints
            return render(request, 'home_tenant.html', context)    
    
    return render(request, 'error.html')

def get_complaint_list(request):
    if request.method =="GET":
        complaint_list = Complaint.objects.all()
        serializer = ComplaintSerializer(complaint_list, many=True)
        return JsonResponse(serializer.data, safe=False)

def upload_rectification(request):
    form = Rectification_Form()
    if request.method == 'POST':
        form = Rectification_Form(request.POST, request.FILES)
        if form.is_valid():
            rec = form.save(commit = False)
            complaintid = request.POST.get('complaintid', -1)
            complaint = Complaint.objects.get(id = complaintid) 
            complaint.tenant_response = rec.tenant_response
            complaint.tenant_picture = rec.tenant_picture
            complaint.status = 'Pending Staff Response'
            complaint.save()
            return redirect('/singhealth/rectifysuccess')
        
    else:
        context = {"form": form}
        return render(request, 'rectify.html', context)
    
    
    
def rectify_success(request):
    complaint = Complaint.objects.last()
    return render(request, 'rectify_success.html', {'complaint': complaint,})


def view_tenant(request):
    context = {}
    if request.method == "POST":
        tenantId = request.POST.get('tenantId', -1)
        staffId = request.POST.get('staffId', -1)
        tenant = Tenant.objects.get(username = tenantId)
        staff = Staff.objects.get(username = staffId)
        complaints = Complaint.objects.filter(staff = staff, tenant = tenant)
        context['tenant'] = tenant
        context['complaints'] = complaints
        return render(request, 'view_complaint.html', context)
        
    return render(request, 'error.html')

