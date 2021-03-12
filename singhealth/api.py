from .models import Complaint
from rest_framework import viewsets, permissions
from .serializer import ComplaintSerializer

#Complaint Viewset
class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    permissions_classes = [
        permissions.AllowAny
    ]
    
    serializer_class = ComplaintSerializer