from django.urls import path
from . import views
from tecwatch import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf.urls import url

urlpatterns = [
    path('export_excel/', views.export_excel, name="export-excel"),
    path('send_email/', views.go_to_email, name="email"),
    path('click_mail/', views.send_mail_plain_with_file, name="click_mail"),
    
]




if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)