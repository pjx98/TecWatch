from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import Complaint_Form
from .models import Complaint

# Create your views here.
def home(request):
    return HttpResponse('Home Page')

def create_complaint(request):
    form = Complaint_Form()
    if request.method == 'POST':
        form = Complaint_Form(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.save()
            return redirect('/singhealth/success')
    context = {"form": form,}
    return render(request, 'create.html', context)


def view_all(request):
    complaints = Complaint.objects.all()
    return render(request, 'view_complaint.html', {'complaints': complaints})

def create_success(request):
    complaint = Complaint.objects.last()
    return render(request, 'complaint_success.html', {'complaint': complaint,})

def login(request):
    return render(request, 'login_buttons.html')

def homestaff(request):
    complaints = Complaint.objects.all()
    return render(request, 'home_staff.html', {'complaints': complaints})
    
    
def hometenant(request):
    complaints = Complaint.objects.all()
    return render(request, 'home_tenant.html', {'complaints': complaints})
    

