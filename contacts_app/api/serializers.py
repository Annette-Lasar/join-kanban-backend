from rest_framework import serializers
from ..models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'first_name', 'last_name', 'email', 'phone_number', 'color', 'color_brightness', 'created_by']
        read_only_fields = ['created_by']
        
        
