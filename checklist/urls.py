from django.urls import path
from . import views
from tecwatch import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf.urls import url

urlpatterns = [
    path('additems/', views.add_items, name="add_items"),
    path('fnb/', views.fnb, name="fnb"),
    path('nonfnb/', views.nonfnb, name="nonfnb"),
    path('update/', views.update_checklist, name="updatechecklist"),
    path('audit/', views.audit, name="audit"),
    path('viewaudits/', views.view_audit, name="view_audit"),
    path('calculatescore/',  views.calculate_score, name="calculatescore"),
]




if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)