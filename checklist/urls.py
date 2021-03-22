from django.urls import path
from . import views
from tecwatch import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf.urls import url
from rest_framework import routers

urlpatterns = [
    path('', views.checklist_home),
    path('additems/', views.add_items),
    path('fnb/', views.fnb),
    path('nonfnb/', views.nonfnb),
    path('update/', views.update_checklist),
    path('calculate/', views.calculate),
    
]




if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)