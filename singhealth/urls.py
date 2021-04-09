from django.urls import path
from . import views
from tecwatch import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf.urls import url


urlpatterns = [
    path('create/', views.create_complaint, name="create"),
    path('homestaff/', views.homestaff, name="homestaff"),
    path('hometenant/', views.hometenant, name="hometenant"),
    path('viewtenant/', views.view_tenant, name="viewtenant"),
    path('viewcomplaint/', views.view_complaint, name="viewcomplaint"),
    path('update/', views.update, name="updatecomplaint"),
    path('updatesuccess/', views.update_success, name="updatesuccess"),
    path('updatesuccesspage/', views.update_success_page, name="updatesuccesspage"),
    url('favicon.ico', RedirectView.as_view(url = '/media/images/')),
    path('', views.loginPage, name="login"),  
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('tenant/', views.tenant, name="tenant"),
    path('staff/', views.staff, name="staff"),
    
]




if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)