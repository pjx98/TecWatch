from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import  CreateUserForm

# from .decorators import unauthenticated_user, allowed_users, admin_only


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
	return render(request, 'accounts/register.html', context)


def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			if user.groups.filter (name='staff'):
				return redirect('staff')
			elif user.groups.filter (name='tenant'):
				return redirect('tenant')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


def staff(request):
	return render(request, 'accounts/staff.html')


def tenant(request):
	return render(request, 'accounts/tenant.html')


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def products(request):
# 	products = Product.objects.all()

# 	return render(request, 'accounts/products.html', {'products':products})

