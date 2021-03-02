from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage),
    path('tenants/', views.tenants),
    path('staff/', views.staff),

]