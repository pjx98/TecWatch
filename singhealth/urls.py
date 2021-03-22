from django.urls import path
from . import views
from tecwatch import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf.urls import url
from rest_framework import routers
from .api import ComplaintViewSet


urlpatterns = [
    path('create/', views.create_complaint),
    path('success/', views.create_success),
    path('login/', views.login),
    path('homestaff/', views.homestaff),
    path('hometenant/', views.hometenant),
    path('viewtenant/', views.view_tenant),
    path('viewcomplaint/', views.view_complaint),
    path('update/', views.update),
    path('updatesuccess/', views.update_success),
    path('successstaff/', views.success_staff),
    path('successtenant/', views.success_tenant),
    url('favicon.ico', RedirectView.as_view(url = '/media/images/')),
    
]




if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)