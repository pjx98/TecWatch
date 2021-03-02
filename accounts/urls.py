from django.urls import path
from . import views

urlpatterns = [
    #path('', views.loginPage),
    path('tenant/', views.tenant, name="tenant"),
    path('staff/', views.staff, name="staff"),
    path('register/', views.registerPage, name="register"),
	path('', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
]