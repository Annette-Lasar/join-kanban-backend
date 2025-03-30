from rest_framework import serializers
from contacts_app.models import Contact
from django.contrib.auth import get_user_model

User = get_user_model()

        

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'repeated_password', 'name', 'phone_number']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
        
    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        email = self.validated_data['email']
        name = self.validated_data['name'].strip()
        
        if pw != repeated_pw:
            raise serializers.ValidationError({'error': 'Passwords do not match.'})
            
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'This email has already been used.'})
        
        name_parts = name.split()
        first_name = name_parts[0] 
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
        
        user = User.objects.create_user(
            username=email,
            email=email,
            password=pw,
            first_name=first_name,
            last_name=last_name
        )
        
        Contact.objects.create(
            name=name,
            email=email,
            phone_number=self.validated_data.get('phone_number', ''),
            created_by=user
        )
            
        return user
        
    

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name"]
        

