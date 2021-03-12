from rest_framework import serializers
from .models import Complaint, Staff, Tenant, Outlet

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'
        




